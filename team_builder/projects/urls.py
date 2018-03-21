from django.conf.urls import url

from . import views

app_name = "projects"

urlpatterns = [
    url(r"(?P<pk>\d+)/", views.ViewProject.as_view(), name="project_view")
]