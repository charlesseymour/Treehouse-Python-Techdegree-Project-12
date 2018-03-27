from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import get_object_or_404

from . import forms, models
from accounts.models import User

class ViewProject(generic.DetailView):
    model = models.Project
    template_name = "projects/project.html"

class EditProject(LoginRequiredMixin, generic.UpdateView):
    model = models.Project
    fields = ['title', 'description', 'estimate', 'requirements']
    template_name = 'projects/project_edit.html'
    
    def get_object(self, *args, **kwargs):
        obj = super(EditProject, self).get_object(*args, **kwargs)
        if obj.created_by != self.request.user:
            raise PermissionDenied()
        return obj
   
    def get_success_url(self, **kwargs):
        return reverse_lazy('projects:project_view', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super(EditProject, self).get_context_data(**kwargs)
        # position_qs = models.Position.objects.filter(project=self.get_object())
        position_formset = forms.PositionInlineFormSet(instance=self.get_object(),
                                                       prefix="positions")
        for subform in position_formset:
            subform.initial['project'] = self.object.id
        context['position_formset'] = position_formset
        return context
        
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        print(self.request.POST)
        formset = forms.PositionInlineFormSet(self.request.POST,
                                              request.FILES,                                              
                                              instance=self.object,
                                              prefix="positions")
        print("form errors = " + str(form.errors))
        print("formset errors = " + str(formset.errors))
        if form.is_valid() and formset.is_valid():
            formset.save()
            return self.form_valid(form)
        return self.form_invalid(form)


class DeleteProject(LoginRequiredMixin, generic.DeleteView):
    model = models.Project
    success_url = reverse_lazy("home")
    
class CreateProject(LoginRequiredMixin, generic.CreateView):
    model = models.Project
    fields = ['title', 'description', 'estimate', 'requirements']
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
        
    def get_success_url(self, **kwargs):
        return reverse_lazy('projects:project_view', kwargs={'pk': self.object.pk})
        
    def get_context_data(self, **kwargs):
        context = super(CreateProject, self).get_context_data(**kwargs)
        position_qs = models.Position.objects.none()
        position_formset = forms.PositionFormSet(queryset=position_qs,
                                                 prefix="positions")
        context['position_formset'] = position_formset
        return context    
     
    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        position_qs = models.Position.objects.none()
        position_formsets = forms.PositionFormSet(self.request.POST,
                                                  queryset=position_qs,
                                                  prefix="positions")
        if form.is_valid():
            project = form.save(commit=False)
            project.created_by = self.request.user
            project.save()
            for fs in position_formsets:
                if fs.is_valid():
                    if 'title' in fs.cleaned_data:
                        position = models.Position(
                            title=fs.cleaned_data['title'],
                            description=fs.cleaned_data['description'],
                            project=project)
                        position.save()
            return self.form_valid(form)
        return self.form_invalid(form)
        
    
    
        
        
# https://stackoverflow.com/questions/26548018/how-to-feed-success-url-with-pk-from-saved-model