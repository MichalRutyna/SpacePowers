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


def get_nation_dropdown(request):
    if request.user.is_authenticated:
        nations = Nation.objects.all()
        response = ""

        response += '<a class="nav-link dropdown-toggle" data-bs-toggle="dropdown" role="button"\
                        aria-haspopup="true" aria-expanded="false">Other nations</a>\
                    <div class="dropdown-menu">'

        for nation in nations:
            url = reverse_lazy('b:other_nations:nation_details', args=(nation.id,))
            name = nation.name

            response += f"<a class='dropdown-item' href='{url}'>{name}</a>"
        summary_url = reverse_lazy('b:other_nations:summary')
        response += f'<div class="dropdown-divider"></div>\
                    <a class="dropdown-item" href="{summary_url}">Summary</a></div>'

        return HttpResponse(response)
    else:
        return HttpResponse("")
