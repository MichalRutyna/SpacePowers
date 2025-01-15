from django.urls import path
from django.views.generic.base import TemplateView


from .views import NationHomeView

app_name = "nation"

urlpatterns = [
    path('', NationHomeView.as_view(), name="home"),
]