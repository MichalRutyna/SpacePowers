from django.http.response import HttpResponse
from django.shortcuts import render
from django.template.context_processors import request
from django.urls.base import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView


from Nation.models import Nation


class NationDetailView(DetailView):
    model = Nation
    template_name = "nation/foreign_detail.html"

class NationSummaryView(ListView):
    model = Nation
    template_name = "nation/foreign_summary.html"
