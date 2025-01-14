from django.urls import path
from django.views.generic.base import TemplateView

from .views import get_nation_dropdown, NationDetailView, NationSummaryView

app_name = "other_nations"

urlpatterns = [
    path('', NationSummaryView.as_view(), name="summary"),
    # api function
    path('nation_list/', get_nation_dropdown, name="nation_list"),
    path('nation/<int:pk>/', NationDetailView.as_view(), name="nation_details"),
]