from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import get_object_or_404

from . import forms, models
from projects.models import Skill, SideProject, Position

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
    
    def get (sef, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)
        
        
        
    
    
    
    
# https://stackoverflow.com/questions/45841951/save-formset-in-an-updateview
# https://docs.djangoproject.com/en/2.0/ref/models/relations/
    
    
