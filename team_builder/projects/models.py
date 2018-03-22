from django.conf import settings
from django.db import models
# Create your models here.

class Project(models.Model):  
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField()
    estimate = models.CharField(max_length=50)
    requirements = models.CharField(max_length=200)
  

class Skill(models.Model):
    user = models.ManyToManyField(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=25, verbose_name="")
    

class Position(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    project = models.ForeignKey(Project,
                                on_delete=models.CASCADE,
                                null=True)
    filled_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  on_delete=models.CASCADE,
                                  null=True)
    skills = models.ManyToManyField(Skill)
    

class SideProject(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             null=True)
    name = models.CharField(max_length=25, verbose_name="")
    url = models.URLField(verbose_name="")