from django.conf import settings
from django.db import models
# Create your models here.

class Skill(models.Model):
    user = models.ManyToManyField(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=25, verbose_name="")
    
    
class Project(models.Model):  
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                        on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField()
    estimate = models.CharField(max_length=50)
    requirements = models.CharField(max_length=200)
    
class SideProject(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             null=True)
    name = models.CharField(max_length=25, verbose_name="")
    url = models.URLField(verbose_name="")