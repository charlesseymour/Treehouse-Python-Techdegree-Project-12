from django.views.generic import ListView

from projects.models import Project, Position

class Home(ListView):
    model = Project
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['position_list'] = Position.objects.all()
        return context