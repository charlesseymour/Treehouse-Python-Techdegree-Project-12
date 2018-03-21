from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import get_object_or_404

from . import forms, models
from accounts.models import User

class ViewProject(generic.DetailView):
    model = models.Project
    template_name = "projects/project.html"
