import os
from django.db import models
from django.conf import settings

from chemflow.jobs.tasks import run_dock, run_score


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

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(Job, self).save(force_insert=False, force_update=False, using=None,
                              update_fields=None)

        workdir = os.path.join(settings.MEDIA_ROOT, 'user_' + self.owner.username)
        print(workdir)
        project_name = self.project_name
        protocol_name = self.protocol
        receptor_file_path = os.path.basename(str(self.receptor_file))
        ligands_file_path = os.path.basename(str(self.ligands_file))
        center_x = str(self.center_x)
        center_y = str(self.center_y)
        center_z = str(self.center_z)
        sf = self.sf
        run_dock.delay(workdir,
                       project_name,
                       protocol_name,
                       receptor_file_path,
                       ligands_file_path,
                       center_x,
                       center_y,
                       center_z,
                       sf)
