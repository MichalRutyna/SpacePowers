from django.urls import path
from django.urls.conf import include
from django.views.generic.base import TemplateView

from .views import SignUpView, LoginView

app_name = "account"

urlpatterns = [
    path('', TemplateView.as_view(template_name="account/profile.html"), name="home"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path('', include("django.contrib.auth.urls")),
]