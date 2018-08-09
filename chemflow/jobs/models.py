from django.db import models
from django.conf import settings


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f'user_{instance.owner.username}/{filename}'


class Job(models.Model):
    job_type = models.CharField(max_length=50, blank=True)
    job_name = models.CharField(max_length=100,  blank=True)
    project_name = models.CharField(max_length=50, blank=True)
    protocol = models.CharField(max_length=50, blank=True)
    sf = models.CharField(max_length=50, default='vina')

    receptor_file = models.FileField(upload_to=user_directory_path)
    receptor_name = models.CharField(max_length=100,  blank=True)
    ligands_file = models.FileField(upload_to=user_directory_path)
    ligands_name = models.CharField(max_length=100, blank=True)

    center_x = models.FloatField(blank=True, null=True)
    center_y = models.FloatField(blank=True, null=True)
    center_z = models.FloatField(blank=True, null=True)

    radius = models.FloatField(blank=True, null=True)

    size_x = models.FloatField(blank=True, null=True)
    size_y = models.FloatField(blank=True, null=True)
    size_z = models.FloatField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True)
    state = models.CharField(max_length=50, default='Q')

    def __str__(self):
        return self.job_name
