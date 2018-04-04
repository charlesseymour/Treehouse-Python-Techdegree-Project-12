from django.views.generic import ListView

from projects.models import Project, Position

class Home(ListView):
    model = Project
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['position_list'] = Position.objects.all()
        context['greeting'] = 'Howdy!'
        return context
        
        
# https://stackoverflow.com/questions/18812505/can-i-have-multiple-lists-in-a-django-generic-listview


    