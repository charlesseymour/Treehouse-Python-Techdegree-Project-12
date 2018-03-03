from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import get_object_or_404

from . import forms, models

class SignUp(generic.CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy("accounts:edit")
    template_name = "accounts/signup.html"
    
    def form_valid(self, form):
        valid = super(SignUp, self).form_valid(form)
        email, password = form.cleaned_data.get('email'), form.cleaned_data.get('password1')
        new_user = authenticate(email=email, password=password)
        login(self.request, new_user)
        return valid
    
class EditProfile(LoginRequiredMixin, generic.UpdateView):
    model = models.User
    fields = ['email', 'first_name', 'last_name', 'full_name', 'about', 'avatar']
    template_name = "accounts/profile_edit.html"
    success_url = "home"
    
    def get_object(self):
        return self.request.user
    


    
    
