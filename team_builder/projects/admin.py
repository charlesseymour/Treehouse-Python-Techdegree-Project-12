from django.contrib import admin

from . import models

admin.site.register(models.Project)
admin.site.register(models.Position)
admin.site.register(models.Skill)
admin.site.register(models.Application)
admin.site.register(models.Notification)
admin.site.register(models.SideProject)
