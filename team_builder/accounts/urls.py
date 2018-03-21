from django.conf.urls import url

from . import views

app_name="accounts"

urlpatterns = [
    url(r"edit/$", views.EditProfile.as_view(), name="edit"),
    url(r"signup/$", views.SignUp.as_view(),  name="signup"),
    url(r"signin/$", views.SignIn.as_view(), name="signin"),
    url(r"signout/$", views.SignOut.as_view(), name="signout"),
    url(r"view/(?P<pk>\d+)/", views.ViewProfile.as_view(), name="view")
]

