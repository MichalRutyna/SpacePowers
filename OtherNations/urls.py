from django.urls import path
from django.views.generic.base import TemplateView

from .views import NationDetailView, NationSummaryView

app_name = "other_nations"

urlpatterns = [
    path('', NationSummaryView.as_view(), name="summary"),
    path('nation/<int:pk>/', NationDetailView.as_view(), name="nation_details"),
]