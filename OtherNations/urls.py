from django.urls import path
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required

from .views import NationDetailView, NationSummaryView

app_name = "other_nations"

urlpatterns = [
    path('', login_required(NationSummaryView.as_view()), name="summary"),
    path('nation/<int:pk>/', login_required(NationDetailView.as_view()), name="nation_details"),
]