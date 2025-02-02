from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from Nation.models import Nation


class OtherNationDetailView(DetailView):
    model = Nation
    template_name = "nation/foreign_detail.html"

class OtherNationSummaryView(ListView):
    model = Nation
    template_name = "nation/foreign_summary.html"
