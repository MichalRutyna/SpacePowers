from django.urls import path

from .views import *

app_name = "nation"

urlpatterns = [
    path('', login_required(NationHomeView.as_view()), name="home"),
    path('<slug:slug>/', login_required(NationDetailView.as_view()), name="details"),
    path('create/', login_required(NationCreateView.as_view()), name="create"),
    path('<slug:nation_slug>/fields/', login_required(ModelFieldEndpoint.as_view()), name="edit"),
]
