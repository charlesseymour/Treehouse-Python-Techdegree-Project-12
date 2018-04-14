from django.conf.urls import url

from . import views

app_name = "projects"

urlpatterns = [
    url(r"^(?P<pk>\d+)/$", views.ViewProject.as_view(), name="project_view"),
    url(r"^edit/(?P<pk>\d+)/$", views.EditProject.as_view(), name="project_edit"),
    url(r"^delete/(?P<pk>\d+)/$", views.DeleteProject.as_view(), name="project_delete"),
    url(r"^new/$", views.CreateProject.as_view(), name="project_create"),
    url(r"^search/$", views.search, name="search")
]