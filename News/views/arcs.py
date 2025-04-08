from django.shortcuts import render
from django.views.generic.base import View
from django.views.generic.edit import UpdateView

from News.models import Arc


class ArcsPageView(View):
    template_name = 'news/pages/manage_arcs.html'

    def get(self, *args, **kwargs):
        context = {
            "arcs": self.request.user.arc_set.all(),
        }
        return render(self.request, self.template_name, context)


class ArcManageAPI(UpdateView):
    model = Arc
    template_name = 'news/pages/_arcs.html'

    def get(self, **kwargs):
        pass