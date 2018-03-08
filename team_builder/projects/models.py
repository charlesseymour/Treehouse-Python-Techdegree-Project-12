from django.conf import settings
from django.db import models
# Create your models here.

class Skill(models.Model):
    name = models.CharField(max_length=25)
    
    
class Project(models.Model):  
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                        on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField()
    estimate = models.CharField(max_length=50)
    requirements = models.CharField(max_length=200)