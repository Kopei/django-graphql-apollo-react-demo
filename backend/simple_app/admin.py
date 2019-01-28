from __future__ import unicode_literals

# Register your models here.
from django.contrib import admin
from . import models

admin.site.register(models.Message)