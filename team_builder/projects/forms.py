from django import forms
from django.forms import inlineformset_factory
from projects import models
from accounts import models as accounts_models
from djangoformsetjs.utils import formset_media_js

'''class PositionForm(forms.ModelForm):
    class Meta:
        model = models.Position
        fields = ['title', 'description', 'skills', 'project']
        
    class Media(object):
        js = formset_media_js'''
        

PositionInlineFormSet =  inlineformset_factory(
    models.Project,
    models.Position,
    # form=PositionForm,
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


# https://stackoverflow.com/questions/22255759/django-forms-dynamic-choices-for-choicefield     
# https://stackoverflow.com/questions/1760421/how-can-i-render-a-manytomanyfield-as-checkboxes
# https://stackoverflow.com/questions/22592276/django-how-to-style-a-checkboxselectmultiple-in-a-form