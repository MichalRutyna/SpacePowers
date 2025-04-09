from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.generic.base import View
from django.views.generic.edit import UpdateView

from News.models import Arc
from News.forms import ArcForm


class ArcsPageView(View):
    template_name = 'news/pages/manage_arcs.html'

    def get(self, *args, **kwargs):
        context = {
            "arcs": self.request.user.arc_set.all(),
        }
        return render(self.request, self.template_name, context)


class ArcManageAPI(UpdateView):
    model = Arc
    template_name = 'news/parts/arc_manage_form.html'
    form_class = ArcForm

    def form_valid(self, form):
        self.object = form.save()
        self.object.slug = slugify(form.cleaned_data['title'])
        messages.add_message(self.request, messages.SUCCESS, 'Arc saved')
        return HttpResponse("", headers={"HX-Refresh": "true"})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
                "arc": self.get_object(),
        })
        return context

    def delete(self, request, *args, **kwargs):
        if self.get_object().posts.exists():
            messages.add_message(self.request, messages.ERROR, 'You cannot delete this arc because it contains posts. If you really want to do this, contact moderation')
            return HttpResponse("", headers={"HX-Refresh": "true"})
        self.get_object().delete()
        messages.add_message(self.request, messages.SUCCESS, 'Arc deleted')
        return HttpResponse("", headers={"HX-Refresh": "true"})

class ArcAddAPI(View):

    def post(self, request, *args, **kwargs):
        title = f"{request.user.username}'s arc ({request.user.arc_set.count()+1})"
        arc_obj = Arc(title=title, slug=slugify(title))
        arc_obj.save()
        arc_obj.users.add(request.user)
        context = {
            "arc": arc_obj
        }
        return render(request, "news/parts/components/arcs_page/arc_manage_pill.html", context)
