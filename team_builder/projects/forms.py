from django import forms
from django.forms import modelformset_factory
from projects import models


PositionFormSet =  modelformset_factory(
    models.Position,
    fields=('title', 'description', 'skills'),
    widgets={'title': forms.TextInput(attrs={'label': '',
                                             'placeholder': 'Position title'}),
             'description': forms.Textarea(attrs={'label': '',
                                           'placeholder': 'Position description'}),
             'skills': forms.CheckboxSelectMultiple()
            })

# https://stackoverflow.com/questions/22255759/django-forms-dynamic-choices-for-choicefield     
# https://stackoverflow.com/questions/1760421/how-can-i-render-a-manytomanyfield-as-checkboxes
# https://stackoverflow.com/questions/22592276/django-how-to-style-a-checkboxselectmultiple-in-a-form