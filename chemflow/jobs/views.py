import os
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView, CreateView, DeleteView
from django.urls import reverse
from django.conf import settings

from .models import Job
from .forms import JobDockForm, JobScoreForm
from chemflow.jobs.tasks import run_dock, run_score


class JobCreateView(LoginRequiredMixin, CreateView):
    model = Job
    slug_field = "job_type"
    slug_url_kwarg = "job_type"

    def post(self, request, *args, **kwargs):
        request.POST = request.POST.copy()
        request.POST['owner'] = request.user.id
        request.POST['state'] = 'Q'
        request.POST['job_name'] = request.POST.get('project_name') + " - " + request.POST.get('protocol')
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
        run_score.delay("test", "file", "file", 1, 2, 3)
        return super(JobCreateScoreView, self).form_valid(form)


job_create_score_view = JobCreateScoreView.as_view()


class JobListView(LoginRequiredMixin, ListView):
    model = Job
    slug_field = "job_name"
    slug_url_kwarg = "job_name"


job_list_view = JobListView.as_view()


class JobDetailView(DetailView):
    model = Job
    slug_field = "job_name"
    slug_url_kwarg = "job_name"


job_detail_view = JobDetailView.as_view()


class JobDeleteView(DeleteView):
    model = Job
    slug_field = "job_name"
    slug_url_kwarg = "job_name"

    def get_success_url(self):
        return reverse("jobs:list")


job_delete_view = JobDeleteView.as_view()
