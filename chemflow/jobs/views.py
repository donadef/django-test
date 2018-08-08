from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView, CreateView, DeleteView

from .models import Job
from .forms import JobForm
from chemflow.jobs.tasks import run_job


class JobCreateView(LoginRequiredMixin, CreateView):
    model = Job
    form_class = JobForm
    success_url = '/jobs/'

    def post(self, request, *args, **kwargs):
        request.POST = request.POST.copy()
        request.POST['job_name'] = request.POST.get('project_name') + " - " + request.POST.get('protocol')
        request.POST['owner'] = request.user.id
        request.POST['state'] = 'Q'
        # call(["DockFlow", "-h"])
        run_job.delay("test", "file", "file", 1, 2, 3)
        return super(JobCreateView, self).post(request, *args, **kwargs)

    # def get_form_kwargs(self):
    #     # pass "user" keyword argument with the current user to your form
    #     kwargs = super(JobCreateView, self).get_form_kwargs()
    #     kwargs['owner'] = self.request.user
    #     return kwargs


job_create_view = JobCreateView.as_view()


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
    success_url = '/jobs/'


job_delete_view = JobDeleteView.as_view()
