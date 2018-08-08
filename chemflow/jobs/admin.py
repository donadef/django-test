from django.contrib import admin
from django.contrib.auth import get_user_model
from django.db import models

from .models import Job


User = get_user_model()
admin.site.register(Job)


