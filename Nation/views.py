from urllib import request

from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.urls.base import reverse_lazy
from django.views.generic.base import View
from django.views.generic.edit import CreateView
from django.template.defaultfilters import slugify

from .forms import *

class NationHomeView(View):
    success_template = 'nation/home.html'
    missing_nation_template = 'nation/no_nation.html'

    def get(self, request):
        context = {}
        try:
            nations = Nation.objects.filter(owner_id=request.user.id)
            context['nations'] = nations
        except Nation.DoesNotExist as e:
            pass

        return render(request, self.success_template, context)


class NationCreateView(UserPassesTestMixin, CreateView):
    form_class = CreateNationForm
    template_name = 'nation/create_nation.html'
    success_url = reverse_lazy("b:nation:home")

    errors = []

    def test_func(self):
        allowed = True
        nation_count = Nation.objects.filter(owner_id=self.request.user.id).count()
        if nation_count > settings.NATION_CREATION_ALLOWED:
            self.errors.append("You control the current maximum allowed number of nations.")
            allowed = False
        if not settings.NATION_CREATION_ALLOWED:
            self.errors.append("An administrator has disabled nation creation.")
            allowed = False
        return allowed

    def handle_no_permission(self):
        context = {"error": "forbidden",
                   "message": "You cannot create a new nation!<br>" + self.errors[0]}

        return render(self.request, 'errors/forbidden.html', context)

    def form_valid(self, form):
        form.instance.owner_id = self.request.user.id
        form.instance.slug = slugify(form.cleaned_data['name'])
        return super().form_valid(form)

