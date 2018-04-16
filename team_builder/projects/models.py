from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from accounts.models import User

class Project(models.Model):  
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField()
    estimate = models.CharField(max_length=50)
    requirements = models.CharField(max_length=200)
    slug = models.SlugField()
    
    #  def get_absolute_url(self):
        #  return reverse('project_view', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Project, self).save(*args, **kwargs)


class Skill(models.Model):
    user = models.ManyToManyField(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=25, verbose_name="")

    def __str__(self):
        return self.name


class Position(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    project = models.ForeignKey(Project,
                                on_delete=models.CASCADE)
    filled_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  on_delete=models.CASCADE,
                                  null=True,
                                  related_name="filled")
    skills = models.ManyToManyField(Skill)
    slug = models.SlugField()
    applicants = models.ManyToManyField(User, through='Application')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Position, self).save(*args, **kwargs)


class SideProject(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             null=True)
    name = models.CharField(max_length=25, verbose_name="")
    url = models.URLField(verbose_name="")


class Application(models.Model):
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)


class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    message = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
