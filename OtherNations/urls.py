from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import *

app_name = "other_nations"


urlpatterns = [
    path('', login_required(OtherNationSummaryView.as_view()), name="summary"),

    path('<slug:slug>/', login_required(OtherNationDetailView.as_view()), name="nation_details"),
]