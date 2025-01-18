from django.urls import path
from django.views.generic.base import TemplateView


from .views import *

app_name = "nation"

urlpatterns = [
    path('', NationHomeView.as_view(), name="home"),
    path('create/', NationCreateView.as_view(), name="create"),
]