from django.urls import path
from django.urls.conf import include
from django.views.generic.base import TemplateView

from .views import SignUpView

app_name = "account"

urlpatterns = [
    path('', TemplateView.as_view(template_name="home.html"), name="home"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path('', include("django.contrib.auth.urls")),
]