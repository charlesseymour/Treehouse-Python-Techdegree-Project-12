from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from django.forms import modelformset_factory
from projects import models

class UserCreateForm(UserCreationForm):
    class Meta:
        fields = ("email", "password1", "password2")
        model = get_user_model()
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].label = "Email Address"
        
SkillFormSet = modelformset_factory(
    models.Skill, 
    fields=('name',),
    widgets={'name': forms.TextInput(attrs={'label': '', 'placeholder': "Skill"})})
