from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import get_object_or_404

from . import forms, models
from projects.models import Skill

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
    formset_class = forms.SkillFormSet
    template_name = "accounts/profile_edit.html"
    success_url = reverse_lazy("home")
    
    def get_object(self):
        return self.request.user
        
    def get_context_data(self, **kwargs):
        context = super(EditProfile, self).get_context_data(**kwargs)
        qs = Skill.objects.filter(user=self.get_object())
        formset = forms.SkillFormSet(queryset=qs)
        context['skill_formset'] = formset
        return context
        
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        qs = Skill.objects.filter(user=self.get_object())
        formsets = forms.SkillFormSet(self.request.POST, queryset=qs)  
        skill_list = []
        if form.is_valid():
            for fs in formsets:
                if fs.is_valid():
                    if 'name' in fs.cleaned_data:
                        try:
                            skill = Skill.objects.get(name__iexact=fs.cleaned_data['name'])
                        except Skill.DoesNotExist:    
                            skill = Skill(name=fs.cleaned_data['name'])
                            skill.save()
                        skill_list.append(skill)
                        '''user = self.object
                        skill = user.skill_set.create(
                            name=fs.cleaned_data['name']
                        )'''
            user = self.object
            user.skill_set.set(skill_list, clear=True)
            return self.form_valid(form)
        return self.form_invalid(form)
        
    
    
# https://stackoverflow.com/questions/45841951/save-formset-in-an-updateview
# https://docs.djangoproject.com/en/2.0/ref/models/relations/
    
    
