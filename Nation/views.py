
from django.http import HttpResponse

from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render, redirect
from django.urls.base import reverse_lazy
from django.views.generic.base import View
from django.views.generic.edit import CreateView

from django.contrib.auth.decorators import login_required

from django.template.defaultfilters import slugify
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.apps import apps

from .forms import *

import logging

logger = logging.getLogger(__name__)


class NationHomeView(View):
    success_template = 'nation/home.html'
    missing_nation_template = 'nation/no_nation.html'

    def get(self, request):
        context = {}
        nations = Nation.objects.filter(owner_id=request.user.id)
        if nations:
            context['nations'] = nations
            return render(request, self.success_template, context)
        else:
            context['nation_creation_enabled'] = settings.NATION_CREATION_ALLOWED
            return render(request, 'nation/no_nation.html', context=context)


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


@csrf_protect
@login_required
def change_to_field(request, nation_slug, field, cnt=0):
    ans = ""
    if request.method == "GET":
        value = getattr(Nation.objects.get(slug=nation_slug), field)
        field_obj = Nation._meta.get_field(field)

        ans += f'<label for="{field}">{field_obj.verbose_name}:</label>\
               <input type="text" id="{field}" name="{field}" value="{value}">'
        return HttpResponse(ans)


    elif request.method == "POST":
        error = ""
        try:
            obj = Nation.objects.get(slug=nation_slug)
            setattr(obj, field, request.POST[field])
            obj.save()
        except ValueError:
            error = "Invalid value!"
        except Exception as e:
            error = str(e)
        if error:
            messages.error(request, error)

        logger.info(f"{request.user} changed {field} to {request.POST[field]} in {nation_slug}")
        return redirect(reverse_lazy("b:nation:home"), extra_context={'error': error})


@csrf_protect
@login_required
def change_variable_model_field(request, parent_id, model_name, pk):
    model = apps.get_model(app_label='Nation', model_name=model_name)
    if request.method == "GET":
        ans = ""
        try:
            instance = model.objects.get(pk=pk)
        except model.DoesNotExist:
            print(model_name)
            if model_name == "army":
                instance = model.objects.create(nation=Nation.objects.get(pk=parent_id))
            elif model_name == "unit":
                instance = model.objects.create(army=Army.objects.get(pk=parent_id))

        for field in model._meta.get_fields():
            if field.is_relation:
                continue
            if field.name in ('id', 'slug'):
                continue
            if field.name == 'army':
                # Future feature - change army allegiance
                continue
            value = getattr(instance, field.name)
            print("ajdi", instance.id)
            ans += f'<label for="{field.name}">{field.verbose_name.capitalize()}:</label>\
                           <input type="text" id="{field.name}" name="{field.name}" value="{value}"> '
        ans += f'<input type="submit" hidden /><input type="number" hidden value="{instance.id}" name="id"/>'
        return HttpResponse(ans)


    elif request.method == "POST":
        error = ""
        try:
            try:
                instance = model.objects.get(pk=pk)
            except model.DoesNotExist:
                instance = model.objects.get(pk=int(request.POST['id']))
            print(request.POST)
            for field, value in request.POST.items():
                if field == "csrfmiddlewaretoken":
                    continue
                setattr(instance, field, value)
            try:
                setattr(instance, 'slug', slugify(request.POST['name']))
            except Exception as e:
                pass
            instance.save()
        except ValueError as e:
            error = "Invalid value!"
            print(e)
        if error:
            messages.error(request, error)

        logger.info(f"{request.user} submitted {request.POST} for {model_name} of pk {pk}")
        return redirect(reverse_lazy("b:nation:home"), extra_context={'error': error})

    elif request.method == "DELETE":
        error = ""
        try:
            instance = model.objects.get(pk=pk)
        except model.DoesNotExist:
            error = "Delete on not existing object"
            return
        try:
            instance.delete()
        except Exception as e:
            pass
        if error:
            messages.error(request, error)

        logger.info(f"{request.user} deleted {request.POST} for {model_name} of pk {pk}")
        return HttpResponse("")

