from django import forms
from django.forms import inlineformset_factory
from projects import models
from accounts import models as accounts_models
from djangoformsetjs.utils import formset_media_js
        

PositionInlineFormSet =  inlineformset_factory(
    models.Project,
    models.Position,
    fields=('title', 'description', 'skills', 'project'),
    extra=0,
    widgets={'title': forms.TextInput(attrs={'label': '',
                                             'placeholder': 'Position title'}),
             'description': forms.Textarea(attrs={'label': '',
                                           'placeholder': 'Position description'}),
             'skills': forms.CheckboxSelectMultiple(),
             'project': forms.HiddenInput()
            }
)

