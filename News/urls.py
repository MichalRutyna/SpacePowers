from django.urls import path
from django.views.generic.base import TemplateView


app_name = "news"

urlpatterns = [
    path('', TemplateView.as_view(template_name="news/home.html"), name="home"),
]