from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect

from . import forms, models
from projects.models import Skill, SideProject, Position, Application, Project

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
    fields = ['full_name', 'about', 'avatar']
    # formset_class = forms.SkillFormSet
    template_name = "accounts/profile_edit.html"
    success_url = reverse_lazy("home")
    
    def get_object(self):
        return self.request.user
        
    def get_context_data(self, **kwargs):
        context = super(EditProfile, self).get_context_data(**kwargs)
        skill_qs = Skill.objects.filter(user=self.get_object())
        skill_formset = forms.SkillFormSet(queryset=skill_qs, prefix="skills")
        context['skill_formset'] = skill_formset
        side_project_qs = SideProject.objects.filter(user=self.get_object())
        side_project_formset = forms.SideProjectFormSet(
                                   queryset=side_project_qs, 
                                   prefix="side_projects")
        context['side_project_formset'] = side_project_formset
        positions = Position.objects.filter(filled_by=self.get_object())
        context['positions'] = positions
        return context
        
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        skill_qs = Skill.objects.filter(user=self.get_object())
        skill_formsets = forms.SkillFormSet(self.request.POST,
                                            queryset=skill_qs,
                                            prefix="skills")  
        skill_list = []
        side_project_qs = SideProject.objects.filter(user=self.get_object())
        side_project_formsets = forms.SideProjectFormSet(self.request.POST,
                                            queryset=side_project_qs,
                                            prefix="side_projects")  
        skill_list = []
        side_project_list = []
        if form.is_valid():
            for fs in skill_formsets:
                if fs.is_valid():
                    if 'name' in fs.cleaned_data:
                        try:
                            skill = Skill.objects.get(name__iexact=fs.cleaned_data['name'])
                        except Skill.DoesNotExist:    
                            skill = Skill(name=fs.cleaned_data['name'])
                            skill.save()
                        skill_list.append(skill)
            user = self.object
            user.skill_set.set(skill_list, clear=True)
            for fs in side_project_formsets:
                if fs.is_valid():
                    if 'name' in fs.cleaned_data:
                        try:
                            side_project = SideProject.objects.get(
                                name__iexact=fs.cleaned_data['name'],
                                url=fs.cleaned_data['url'],
                                user=user)
                        except SideProject.DoesNotExist:
                            side_project = SideProject(
                                name=fs.cleaned_data['name'],
                                url=fs.cleaned_data['url'],
                                user=user)
                            side_project.save()
                        side_project_list.append(side_project)
            user.sideproject_set.set(side_project_list, clear=True)
            return self.form_valid(form)
        return self.form_invalid(form)
        
class SignIn(generic.FormView):
    form_class = AuthenticationForm
    success_url = reverse_lazy("home")
    template_name = "accounts/signin.html"
    
    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(self.request, **self.get_form_kwargs())
        
    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)
        
class SignOut(generic.RedirectView):
    url = reverse_lazy("home")
    
    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)
        
class ViewProfile(generic.DetailView):
    model = models.User
    template_name = "accounts/profile.html"
    
    def get_context_data(self, **kwargs):
        context = super(ViewProfile, self).get_context_data(**kwargs)
        if self.request.user:
            context['user'] = self.request.user
        return context
    
class ViewApplications(LoginRequiredMixin, generic.ListView):
    model = Application
    template_name = 'accounts/applications.html'
    
    def get_queryset(self):
        qs = super(ViewApplications, self).get_queryset()
        qs = qs.filter(position__project__created_by=self.request.user)
        if self.kwargs.get('filter'):
            if self.kwargs.get('filter') == 'stat':
                return qs.filter(status=self.kwargs.get('slug'))
            elif self.kwargs.get('filter') == 'proj':
                return qs.filter(position__project__title=self.kwargs.get('slug'))
            else:
                return qs.filter(position__title=self.kwargs.get('slug'))
        return qs
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project_list'] = Project.objects.filter(created_by=self.request.user)
        context['project_needs'] = Position.objects.filter(project__created_by=self.request.user)
        if self.kwargs.get('filter'):
            context['filter'] = self.kwargs.get('filter')
            context['slug'] = self.kwargs.get('slug')
        return context
    

class UpdateApplication(LoginRequiredMixin, generic.DetailView):
    model = Application
    template_name = 'accounts/application_confirm.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['decision'] = self.kwargs.get('decision')
        return context
        
    def post(self, request, **kwargs):
        self.object = self.get_object()
        decision = self.kwargs.get('decision')
        success_url = reverse_lazy('accounts:applications_view')
        if decision == 'accept':
            Application.objects.filter(id=self.object.id).update(status='accepted')
            Application.objects.exclude(id=self.object.id).update(status='rejected')
        elif decision == 'reject':
            Application.objects.filter(id=self.object.id).update(status='rejected')
        messages.success(request, "The application was updated!")
        return HttpResponseRedirect(success_url)
            
    
    
# https://stackoverflow.com/questions/30691591/update-object-in-form-view-without-any-fields-in-django


    
    
