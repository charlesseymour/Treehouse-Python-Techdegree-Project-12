from django.views.generic import ListView

from projects.models import Project, Position


class Home(ListView):
    model = Project
    template_name = 'index.html'

    def get_queryset(self):
        qs = super(Home, self).get_queryset().order_by('-id')
        if self.kwargs.get('slug'):
            return qs.filter(position__slug__exact=self.kwargs['slug'])
        else:
            return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['position_list'] = Position.objects.values('title',
                                                           'slug').distinct()
        if self.kwargs.get('slug'):
            context['slug'] = self.kwargs['slug']
        return context
