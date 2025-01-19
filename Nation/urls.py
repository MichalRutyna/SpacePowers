from django.urls import path
from django.views.generic.base import TemplateView


from .views import *

app_name = "nation"

urlpatterns = [
    path('', NationHomeView.as_view(), name="home"),
    path('create/', NationCreateView.as_view(), name="create"),
    path('edit/<str:model_name>/<int:pk>/', change_variable_model_field, name="edit"),
    path('edit/<slug:nation_slug>/<str:field>/', change_to_field, name="edit"),
]