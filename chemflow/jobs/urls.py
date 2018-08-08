from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from chemflow.jobs.views import (
    job_list_view,
    job_create_view,
    job_detail_view,
    job_delete_view
)

app_name = "jobs"
urlpatterns = [
    path("", view=job_list_view, name="list"),
    path("new", view=job_create_view, name="create"),
    path("<str:pk>/", view=job_detail_view, name="detail"),
    path("<str:pk>/delete", view=job_delete_view, name="delete"),
]

urlpatterns += staticfiles_urlpatterns()
