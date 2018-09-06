import os
import shutil
import tarfile
from wsgiref.util import FileWrapper
import mimetypes

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView, CreateView, DeleteView
from django.urls import reverse
from django.conf import settings
from django.http import HttpResponse
from django.utils.encoding import smart_str

from .models import Job
from .forms import JobDockForm, JobScoreForm
from .tasks import run_dock, run_score, postprocess_dock, postprocess_score


class JobCreateView(LoginRequiredMixin, CreateView):
    model = Job
    slug_field = "job_type"
    slug_url_kwarg = "job_type"

    def post(self, request, *args, **kwargs):
        request.POST = request.POST.copy()
        request.POST['owner'] = request.user.id
        request.POST['state'] = '0'
        request.POST['job_name'] = request.POST.get('project_name') + " - " + request.POST.get('protocol_name')
        request.POST['receptor_name'] = str(request.FILES['receptor_file']).split('.')[0]
        request.POST['ligands_name'] = str(request.FILES['ligands_file']).split('.')[0]
        return super(JobCreateView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("jobs:list")

    def form_valid(self, form):
        user_jobs = list(Job.objects.filter(owner=self.request.user,
                                            job_type=self.request.POST.get('job_type'),
                                            job_name=self.request.POST.get('job_name')))
        if len(user_jobs) > 0:
            form.add_error('job_name', u'You already have a job with the same name. Please change the project or protocol name.')
            return self.form_invalid(form)

        return super(JobCreateView, self).form_valid(form)


class JobCreateDockView(JobCreateView):
    form_class = JobDockForm

    def post(self, request, *args, **kwargs):
        request.POST = request.POST.copy()
        request.POST['job_type'] = 'dock'

        return super(JobCreateDockView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        return super(JobCreateDockView, self).form_valid(form)


job_create_dock_view = JobCreateDockView.as_view()


class JobCreateScoreView(JobCreateView):
    form_class = JobScoreForm

    def post(self, request, *args, **kwargs):
        request.POST = request.POST.copy()
        request.POST['job_type'] = 'score'

        return super(JobCreateScoreView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        return super(JobCreateScoreView, self).form_valid(form)


job_create_score_view = JobCreateScoreView.as_view()


class JobListView(LoginRequiredMixin, ListView):
    model = Job
    slug_field = "job_name"
    slug_url_kwarg = "job_name"

    def get(self, request, *args, **kwargs):
        for object in self.get_queryset():
            if object.state == '0':
                workdir = os.path.join(settings.MEDIA_ROOT, 'user_' + object.owner.username)
                project_name = object.project_name
                protocol_name = object.protocol_name
                receptor_file_path = os.path.basename(str(object.receptor_file))
                ligands_file_path = os.path.basename(str(object.ligands_file))
                center_x = str(object.center_x)
                center_y = str(object.center_y)
                center_z = str(object.center_z)
                sf = object.sf
                if object.job_type == 'dock':
                    job = run_dock.delay(workdir,
                                         project_name,
                                         protocol_name,
                                         receptor_file_path,
                                         ligands_file_path,
                                         center_x,
                                         center_y,
                                         center_z,
                                         sf)
                else:
                    job = run_score.delay(workdir,
                                          project_name,
                                          protocol_name,
                                          receptor_file_path,
                                          ligands_file_path,
                                          center_x,
                                          center_y,
                                          center_z,
                                          sf)
                # TODO: put the PENDING status here and change it to RUNNING when the task is RUNNING (task.py)
                object.state = "RUNNING"
                object.job_task = str(job)
                object.save()
            else:
                object.save()
        return super(JobListView, self).get(request, *args, **kwargs)


job_list_view = JobListView.as_view()


class JobDetailView(LoginRequiredMixin, DetailView):
    model = Job
    slug_field = "job_name"
    slug_url_kwarg = "job_name"

    def get(self, request, *args, **kwargs):
        object = self.get_object()
        object.save()
        workdir = os.path.join(settings.MEDIA_ROOT, 'user_' + object.owner.username)
        receptor_file_path = os.path.basename(str(object.receptor_file))
        ligands_file_path = os.path.basename(str(object.ligands_file))

        if request.GET.get('postprocess'):
            if object.job_type == 'dock':
                postprocess = postprocess_dock.delay(workdir,
                                                     object.project_name,
                                                     object.protocol_name,
                                                     receptor_file_path,
                                                     ligands_file_path,
                                                     object.center_x,
                                                     object.center_y,
                                                     object.center_z,
                                                     object.sf)
            else:
                postprocess = postprocess_score.delay(workdir,
                                                      object.project_name,
                                                      object.protocol_name,
                                                      receptor_file_path,
                                                      ligands_file_path,
                                                      object.center_x,
                                                      object.center_y,
                                                      object.center_z,
                                                      object.sf)
            object.postprocess_task = str(postprocess)
            object.state = 'POST PROCESSING'
            object.save()

        if request.GET.get('download'):
            pass
            # Compress the results in a tar file
            # tar = tarfile.open("sample.tar.bz2", "w:bz2")
            # for name in ["file1", "file2", "file3"]:
            #     tar.add(name)
            # tar.close()

        if request.GET.get('download_receptor'):
            file_path = os.path.join(workdir, receptor_file_path)
            file_wrapper = FileWrapper(open(file_path, 'rb'))
            file_mimetype = mimetypes.guess_type(file_path)
            response = HttpResponse(file_wrapper, content_type=file_mimetype)
            response['X-Sendfile'] = file_path
            response['Content-Length'] = os.stat(file_path).st_size
            response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(object.receptor_name + '.' + receptor_file_path.split('.')[-1])
            return response

        if request.GET.get('download_ligands'):
            file_path = os.path.join(workdir, ligands_file_path)
            file_wrapper = FileWrapper(open(file_path, 'rb'))
            file_mimetype = mimetypes.guess_type(file_path)
            response = HttpResponse(file_wrapper, content_type=file_mimetype)
            response['X-Sendfile'] = file_path
            response['Content-Length'] = os.stat(file_path).st_size
            response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(object.ligands_name + '.' + ligands_file_path.split('.')[-1])
            return response

        if request.GET.get('download_docking'):
            file_path = os.path.join(workdir, object.project_name + '.chemflow', 'DockFlow', object.protocol_name, receptor_file_path.split('.')[0], 'docked_ligands.mol2')
            file_wrapper = FileWrapper(open(file_path, 'rb'))
            file_mimetype = mimetypes.guess_type(file_path)
            response = HttpResponse(file_wrapper, content_type=file_mimetype)
            response['X-Sendfile'] = file_path
            response['Content-Length'] = os.stat(file_path).st_size
            response['Content-Disposition'] = 'attachment; filename=%s' % smart_str('docked_ligands.mol2')
            return response

        if request.GET.get('download_energy'):
            if object.job_type == 'dock':
                file_path = os.path.join(workdir, object.project_name + '.chemflow', 'DockFlow', object.protocol_name, receptor_file_path.split('.')[0], 'DockFlow.csv')
                file_name = 'DockFlow.csv'
            else:
                file_path = os.path.join(workdir, object.project_name + '.chemflow', 'ScoreFlow', object.protocol_name, receptor_file_path.split('.')[0], 'ScoreFlow.csv')
                file_name = 'ScoreFlow.csv'
            file_wrapper = FileWrapper(open(file_path, 'rb'))
            file_mimetype = mimetypes.guess_type(file_path)
            response = HttpResponse(file_wrapper, content_type=file_mimetype)
            response['X-Sendfile'] = file_path
            response['Content-Length'] = os.stat(file_path).st_size
            response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(file_name)
            return response

        return super(JobDetailView, self).get(request, *args, **kwargs)


job_detail_view = JobDetailView.as_view()


class JobDeleteView(LoginRequiredMixin, DeleteView):
    model = Job
    slug_field = "job_name"
    slug_url_kwarg = "job_name"

    def delete(self, request, *args, **kwargs):
        object = self.get_object()

        # # Remove the receptor and ligands files
        # # TODO: if the file already exist, don't create a new one. Warning, the file must be named using hash of the content (cause file names doesn't mean anything).
        # os.remove(os.path.join(settings.MEDIA_ROOT, str(object.receptor_file)))
        # os.remove(os.path.join(settings.MEDIA_ROOT, str(object.ligands_file)))
        #
        # # Check if there is more than one protocol in the project.
        # if object.job_type == 'dock':
        #     jtype = 'DockFlow'
        #     other = 'ScoreFlow'
        # else:
        #     jtype = 'ScoreFlow'
        #     other = 'DockFlow'
        #
        # project_path = os.path.join(settings.MEDIA_ROOT, 'user_' + object.owner.username, str(object.project_name) + '.chemflow')
        # if len(os.listdir(os.path.join(project_path, jtype))) == 1:
        #     if not os.path.isdir(os.path.join(project_path, other)):
        #         shutil.rmtree(project_path)
        #     else:
        #         shutil.rmtree(os.path.join(project_path, jtype))
        # else:
        #     shutil.rmtree(os.path.join(project_path, jtype, str(object.protocol_name)))
        return super(JobDeleteView, self).delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse("jobs:list")


job_delete_view = JobDeleteView.as_view()
