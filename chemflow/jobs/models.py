from django.db import models
from django.conf import settings


SF_CHOICES = (
    ('vina', 'Vina'),
    ('chemplp', 'ChemPLP'),
    ('plp95', 'plp95'),
    ('plp', 'plp'),
    ('mmgbsa', 'MM-GBSA'),
    ('mmpbsa', 'MM-PBSA')
)

STATE_CHOICES = (
    ('Q', 'Q'),
    ('R', 'R'),
    ('D', 'D')
)


class Job(models.Model):
    job_name = models.CharField(max_length=100, unique=True)
    project_name = models.CharField(max_length=50, blank=True)
    protocol = models.CharField(max_length=50, blank=True)
    sf = models.CharField(max_length=50, choices=SF_CHOICES, default='vina')

    receptor_file = models.CharField(max_length=100, blank=True)
    ligands_file = models.CharField(max_length=100, blank=True)

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
    state = models.CharField(max_length=50, choices=STATE_CHOICES, default='Q')

    def __str__(self):
        return self.job_name
