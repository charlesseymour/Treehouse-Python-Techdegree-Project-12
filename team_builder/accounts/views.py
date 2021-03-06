from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect

from . import forms, models
from projects.models import (Skill, SideProject, Position, Application,
                             Project, Notification)


class SignUp(generic.CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy("accounts:edit")
    template_name = "accounts/signup.html"

    def form_valid(self, form):
        valid = super(SignUp, self).form_valid(form)
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password1')
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
        side_project_formsets = forms.SideProjectFormSet(
                                    self.request.POST,
                                    queryset=side_project_qs,
                                    prefix="side_projects")
        skill_list = []
        side_project_list = []
        if (form.is_valid() and skill_formsets.is_valid() and
            side_project_formsets.is_valid()):
            for fs in skill_formsets:
                if fs.is_valid():
                    if 'name' in fs.cleaned_data:
                        try:
                            skill = Skill.objects.get(
                                        name__iexact=fs.cleaned_data['name']
                                    )
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
        return self.form_invalid(form, skill_formsets, side_project_formsets)
        
    def form_invalid(self, form, skill_formset, side_project_formset):
        return render(self.request,
                      'accounts/profile_edit.html',
                      {'object': self.object,
                       'form': form,
                       'skill_formset': skill_formset,
                       'side_project_formset': side_project_formset,
                       'skill_formset_errors': skill_formset.errors,
                       'side_project_formset_errors': side_project_formset.errors
                       })


class SignIn(LoginView):
    template_name = "accounts/signin.html"


class SignOut(generic.RedirectView):
    url = reverse_lazy("home")

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


@login_required
def account_redirect(request):
    return redirect('accounts:view', pk=request.user.pk)


class ViewProfile(generic.DetailView):
    model = models.User
    template_name = "accounts/profile.html"

    def get_context_data(self, **kwargs):
        context = super(ViewProfile, self).get_context_data(**kwargs)
        if self.request.user:
            context['user'] = self.request.user
        return context


class CreateApplication(LoginRequiredMixin, SuccessMessageMixin,
                        generic.CreateView):
    model = Application
    success_url = reverse_lazy('home')
    form_class = forms.ApplicationCreateForm
    template_name = 'accounts/application_submit.html'

    def get_initial(self, **kwargs):
        return {'position': self.kwargs.get('pk'),
                'applicant': self.request.user,
                'status': 'undecided'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['position_title'] = Position.objects.get(
                                        id=self.kwargs.get('pk')
                                    ).title
        return context

    def form_valid(self, form):
        position = Position.objects.get(id=self.kwargs.get('pk'))
        applicant = self.request.user
        if self.get_queryset().filter(position=position, applicant=applicant):
            messages.error(self.request,
                           'You have already applied for that position')
            return HttpResponseRedirect(reverse_lazy('home'))
        else:
            self.object = form.save()
            messages.success(self.request,
                             'You have applied for the position!')
            return HttpResponseRedirect(self.get_success_url())


class ViewApplications(LoginRequiredMixin, generic.ListView):
    model = Application
    template_name = 'accounts/applications.html'

    def get_queryset(self):
        qs = super(ViewApplications, self).get_queryset().order_by('-id')
        qs = qs.filter(position__project__created_by=self.request.user)
        if self.kwargs.get('filter'):
            if self.kwargs.get('filter') == 'stat':
                return qs.filter(status=self.kwargs.get('slug'))
            elif self.kwargs.get('filter') == 'proj':
                return qs.filter(
                              position__project__title=self.kwargs.get('slug')
                       )
            else:
                return qs.filter(position__title=self.kwargs.get('slug'))
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project_list'] = Project.objects.filter(
                                      created_by=self.request.user
                                  )
        context['project_needs'] = Position.objects.filter(
                                       project__created_by=self.request.user
                                   )
        if self.kwargs.get('filter'):
            context['filter'] = self.kwargs.get('filter')
            context['slug'] = self.kwargs.get('slug')
        return context


class UpdateApplication(LoginRequiredMixin, generic.DetailView):
    model = Application
    template_name = 'accounts/application_confirm.html'

    def get_object(self, queryset=None):
        obj = super(UpdateApplication, self).get_object(queryset=queryset)
        if obj.position.project.created_by != self.request.user:
            raise PermissionDenied
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['decision'] = self.kwargs.get('decision')
        return context

    def post(self, request, **kwargs):
        self.object = self.get_object()
        decision = self.kwargs.get('decision')
        success_url = reverse_lazy('accounts:applications_view')
        if decision == 'accept':
            Application.objects.filter(
                id=self.object.id
            ).update(
                status='accepted'
            )
            Position.objects.filter(
                id=self.object.position.id
            ).update(
                filled_by=self.object.applicant
            )
        elif decision == 'reject':
            Application.objects.filter(
                id=self.object.id
            ).update(
                status='rejected'
            )
        Notification.objects.create(user=self.object.applicant,
                                    message='''You have been {}ed for the position
                                    of {} on the project {}.'''.format(
                                        decision,
                                        self.object.position.title,
                                        self.object.position.project.title
                                        )
                                    )
        messages.success(request, "The application was updated!")
        return HttpResponseRedirect(success_url)


class ViewNotifications(LoginRequiredMixin, generic.ListView):
    model = Notification
    template_name = 'accounts/notification_list.html'

    def get_queryset(self):
        qs = super(ViewNotifications, self).get_queryset()
        qs = qs.filter(user=self.request.user).order_by('-created_date')
        return qs
