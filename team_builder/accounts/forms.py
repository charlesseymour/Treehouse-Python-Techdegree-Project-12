from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from django.forms import ModelForm, modelformset_factory
from projects import models


class UserCreateForm(UserCreationForm):
    class Meta:
        fields = ("email", "password1", "password2")
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].label = "Email Address"


class ApplicationCreateForm(ModelForm):
    class Meta:
        model = models.Application
        fields = ('applicant', 'position', 'status')
        widgets = {'applicant': forms.HiddenInput,
                   'position': forms.HiddenInput,
                   'status': forms.HiddenInput}


SkillFormSet = modelformset_factory(
    models.Skill,
    fields=('name',),
    widgets={'name': forms.TextInput(attrs={'label': '',
                                            'placeholder': "Skill"})})

SideProjectFormSet = modelformset_factory(
    models.SideProject,
    fields=('name', 'url'),
    widgets={'name': forms.TextInput(attrs={'label': '',
                                            'placeholder': "Name"}),
             'url': forms.TextInput(attrs={'label': '',
                                           'placeholder': "URL"})})
