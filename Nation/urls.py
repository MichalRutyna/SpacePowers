from django.urls import path

from .views import *
from django.contrib.auth.decorators import login_required

app_name = "nation"

urlpatterns = [
    path('', login_required(NationHomeView.as_view()), name="home"),

    path('<slug:slug>/', NationDetailView.as_view(), name="details"),

    path('<slug:nation_slug>/fields/', login_required(ModelFieldEndpoint.as_view()), name="edit"),
]
