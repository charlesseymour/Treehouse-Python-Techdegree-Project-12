from django import forms
from django.forms import modelformset_factory
from projects import models

PositionFormSet =  modelformset_factory(
    models.Position,
    fields=('title', 'description'),
    widgets={'title': forms.TextInput(attrs={'label': '',
                                             'placeholder': 'Position title'}),
             'description': forms.Textarea(attrs={'label': '',
                                           'placeholder': 'Position description'})
            })
