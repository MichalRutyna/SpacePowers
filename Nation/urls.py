from django.urls import path
from django.views.generic.base import TemplateView


from .views import *
from django.contrib.auth.decorators import login_required

app_name = "nation"

urlpatterns = [
    path('', login_required(NationHomeView.as_view()), name="home"),
    path('create/', login_required(NationCreateView.as_view()), name="create"),
    path('edit/<int:parent_id>/<str:model_name>/<int:pk>/', change_variable_model_field, name="edit"),
    path('edit/<slug:nation_slug>/<str:field>/', change_to_field, name="edit"),
]