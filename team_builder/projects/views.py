from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.db.models import Q

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
        formset = forms.PositionInlineFormSet(self.request.POST,
                                              request.FILES,                                              
                                              instance=self.object,
                                              prefix="positions")
        if form.is_valid() and formset.is_valid():
            formset.save()
            return self.form_valid(form)
        return self.form_invalid(form, formset)
        
    def form_invalid(self, form, formset):
        return render(self.request,        
                      'projects/project_edit.html', 
                      {'object': self.object,
                       'form':form,
                       'position_formset':formset,
                       'formset_errors': formset.errors})


class DeleteProject(LoginRequiredMixin, generic.DeleteView):
    model = models.Project
    success_url = reverse_lazy("home")
    
class CreateProject(LoginRequiredMixin, generic.CreateView):
    model = models.Project
    fields = ['title', 'description', 'estimate', 'requirements']
    login_url = reverse_lazy("accounts:signin")
        
    def get_success_url(self, **kwargs):
        return reverse_lazy('projects:project_view', kwargs={'pk': self.object.pk})
        
    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        position_formset = forms.PositionInlineFormSet(prefix="positions")
        return render(self.request,
                      'projects/project_form.html',
                      {'form':form, 'position_formset':position_formset})
      
     
    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        formset = forms.PositionInlineFormSet(self.request.POST,
                                              prefix="positions")
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        return self.form_invalid(form, formset)
        
    def form_valid(self, form, formset):
        form.instance.created_by = self.request.user
        self.object = form.save()
        formset.instance = self.object
        formset.save()
        return HttpResponseRedirect(self.get_success_url())
        
    def form_invalid(self, form, formset):
        return render(self.request,
                      'projects/project_form.html',
                      {'form':form,
                       'position_formset':formset,
                       'formset_errors': formset.errors})
      
def search(request):
    term = request.GET.get('q')
    projects = models.Project.objects.filter(
        Q(title__icontains=term) |
        Q(description__icontains=term)
    )
    positions = models.Position.objects.filter(project__in=projects)
    return render(request, 'projects/search.html', {
                 'projects': projects,
                 'term': term,
                 'position_list': positions})
    
    
        
        
# https://stackoverflow.com/questions/36946290/inline-form-validation-returns-empty-formset-errors-list


