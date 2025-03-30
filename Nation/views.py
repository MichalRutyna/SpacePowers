from django.core.exceptions import ValidationError
from django.http import HttpResponse

from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http.request import QueryDict
from django.shortcuts import render, redirect
from django.urls.base import reverse_lazy, reverse
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

from django.template.defaultfilters import slugify
from django.contrib import messages
from django.apps import apps

from .forms import *
from .models import Nation, Ownership

import logging

logger = logging.getLogger(__name__)


def get_user_nations(user):
    nations = user.ownerships.values_list('nation', flat=True)
    nations = Nation.objects.filter(id__in=nations)
    return nations


class NationHomeView(View):
    success_template = 'nation/home.html'
    missing_nation_template = 'nation/no_nation.html'

    def get(self, request):
        context = {}
        nations = get_user_nations(request.user)
        if nations:
            if nations.count() == 1:
                return redirect('b:nation:details', slug= nations[0].slug)
            else:
                context['nations'] = nations
                return render(request, self.success_template, context)
        else:
            context['nation_creation_enabled'] = (settings.NATION_CREATION_ALLOWED and self.request.user.has_perm('Nation.add_nation')) or self.request.user.is_staff
            return render(request, self.missing_nation_template, context=context)


class NationDetailView(UserPassesTestMixin, DetailView):
    model = Nation
    template_name = 'nation/details.html'

    errors = []

    def test_func(self):
        if self.request.user.is_staff:
            return True

        allowed = True
        if not self.get_object().is_user_an_owner(self.request.user):
            allowed = False
        return allowed

    def handle_no_permission(self):
        return redirect(reverse_lazy('b:other_nations:nation_details', kwargs={'slug': self.get_object().slug}))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['edition_allowed'] = (settings.NATION_EDITION_ALLOWED and self.request.user.has_perm('Nation.change_nation')) or self.request.user.is_staff
        return context



class NationCreateView(UserPassesTestMixin, CreateView):
    form_class = CreateNationForm
    template_name = 'nation/create_nation.html'
    success_url = reverse_lazy("b:nation:home")

    errors = []

    def test_func(self):
        if self.request.user.is_staff:
            return True
        allowed = True
        nation_count = self.request.user.ownerships.count()
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

        return render(self.request, '403.html', context)

    def form_valid(self, form):
        form.instance.slug = slugify(form.cleaned_data['name'])
        x = super().form_valid(form)
        Ownership(user=self.request.user, nation=self.object, owner_title=form.cleaned_data['owner_title']).save()
        return x


class ModelFieldEndpoint(UserPassesTestMixin, View):
    errors = []

    def test_func(self):
        if self.request.user.is_staff:
            return True

        allowed = True
        if not settings.NATION_EDITION_ALLOWED:
            allowed = False
            logging.warning(f"{self.request.user} tried to edit a nation when edition was disabled, probably request forgery")
            self.errors.append("An administrator has disabled nation creation.")

        if not self.request.user.has_perm('Nation.change_nation'):
            allowed = False
            logging.warning(f"{self.request.user} tried to edit a nation without permissions, probably request forgery")
            self.errors.append("You don't have permission to edit a nation.")

        # Maybe spam protection here

        # TODO check if owns this nation

        return allowed

    def handle_no_permission(self):
        context = {"error": "forbidden",
                   "message": "You cannot edit nation now!<br>" + self.errors[0]}

    def get(self, *args, **kwargs):
        fields = self.request.GET.getlist('field_slugs')
        model = apps.get_model(app_label='Nation', model_name=self.request.GET['model_slug'])
        instance = model.objects.get(pk=self.request.GET['instance_pk'])

        ans = '<span class="me-auto my-auto align-middle">'
        for field in fields:
            field_value = getattr(instance, field)
            # We're using a protected member correctly, verbose_name is intended to be used in labels
            verbose_name = model._meta.get_field(field).verbose_name
            ans += f'<label class="my-auto" for="{field}">{verbose_name}:</label>\
                   <input type="text" id="{field}" name="{field}" value="{field_value}"> '

        ans += f"""
                </span>
                <button class="btn btn-outline-success m-1 hover_darken_content" type="submit">
                    <!-- Uploaded to: SVG Repo, www.svgrepo.com, Generator: SVG Repo Mixer Tools -->
                    <svg fill="#5cb85c" width="17px" height="21px" viewBox="0 4 96 96" xmlns="http://www.w3.org/2000/svg">
                        <title/>
                        <g>
                            <path d="M58.3945,32.1563,42.9961,50.625l-5.3906-6.4629a5.995,5.995,0,1,0-9.211,7.6758l9.9961,12a5.9914,5.9914,0,0,0,9.211.0059l20.0039-24a5.9988,5.9988,0,1,0-9.211-7.6875Z"/>
                            <path d="M48,0A48,48,0,1,0,96,48,48.0512,48.0512,0,0,0,48,0Zm0,84A36,36,0,1,1,84,48,36.0393,36.0393,0,0,1,48,84Z"/>
                        </g>
                    </svg>
                </button>
                <button class="btn btn-outline-warning m-1 hover_darken_content" type="reset">
                    <!-- Uploaded to: SVG Repo, www.svgrepo.com, Generator: SVG Repo Mixer Tools -->
                    <svg width="17px" height="17px" viewBox="0 1 15 15" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path
                        fill-rule="evenodd"
                        clip-rule="evenodd"
                        d="M4.85355 2.14645C5.04882 2.34171 5.04882 2.65829 4.85355 2.85355L3.70711 4H9C11.4853 4 13.5 6.01472 13.5 8.5C13.5 10.9853 11.4853 13 9 13H5C4.72386 13 4.5 12.7761 4.5 12.5C4.5 12.2239 4.72386 12 5 12H9C10.933 12 12.5 10.433 12.5 8.5C12.5 6.567 10.933 5 9 5H3.70711L4.85355 6.14645C5.04882 6.34171 5.04882 6.65829 4.85355 6.85355C4.65829 7.04882 4.34171 7.04882 4.14645 6.85355L2.14645 4.85355C1.95118 4.65829 1.95118 4.34171 2.14645 4.14645L4.14645 2.14645C4.34171 1.95118 4.65829 1.95118 4.85355 2.14645Z"
                        fill="#ffc107"
                      />
                    </svg>
                </button>
                <a href={reverse_lazy("b:nation:details", kwargs={"slug": self.kwargs['nation_slug']})}><button class="btn btn-outline-danger m-1 hover_darken_content" type="button">
                    <!-- Uploaded to: SVG Repo, www.svgrepo.com, Generator: SVG Repo Mixer Tools -->
                    <svg fill="#d9534f" width="17px" height="21px" viewBox="0 4 96 96" xmlns="http://www.w3.org/2000/svg">
                        <title/>
                        <g>
                            <path d="M48,0A48,48,0,1,0,96,48,48.0512,48.0512,0,0,0,48,0Zm0,84A36,36,0,1,1,84,48,36.0393,36.0393,0,0,1,48,84Z"/>
                            <path d="M64.2422,31.7578a5.9979,5.9979,0,0,0-8.4844,0L48,39.5156l-7.7578-7.7578a5.9994,5.9994,0,0,0-8.4844,8.4844L39.5156,48l-7.7578,7.7578a5.9994,5.9994,0,1,0,8.4844,8.4844L48,56.4844l7.7578,7.7578a5.9994,5.9994,0,0,0,8.4844-8.4844L56.4844,48l7.7578-7.7578A5.9979,5.9979,0,0,0,64.2422,31.7578Z"/>
                        </g>
                    </svg>
                </button></a> """

        return HttpResponse(ans)

    def put(self, *args, **kwargs):
        data = QueryDict(self.request.body)
        fields = data.getlist('field_slugs')
        model = apps.get_model(app_label='Nation', model_name=data.get('model_slug'))
        instance = model.objects.get(pk=data.get('instance_pk'))

        previous_values = []
        changed_values = []
        # could be changed for each field if need arises
        for field in fields:
            prev_value = getattr(instance, field)
            previous_values.append(prev_value)

            new_value = data.get(field)
            setattr(instance, field, new_value)
            changed_values.append(new_value)

        try:
            instance.full_clean()
            instance.save()
        except ValidationError as e:
            for error in e.messages:
                messages.error(self.request, error)

        logger.info(
            f"{self.request.user} changed {fields} of {model} ({self.kwargs["nation_slug"]}) from {previous_values} to {changed_values}")
        return HttpResponse("", headers={"HX-Refresh": "true"})

    def post(self, *args, **kwargs):
        data = QueryDict(self.request.body)
        model = apps.get_model(app_label='Nation', model_name=data.get('model_slug'))
        parent_model = apps.get_model(app_label='Nation', model_name=data.get('parent_model_slug'))

        instance = model()
        setattr(instance, data.get('parent_model_slug'), parent_model.objects.get(pk=data.get('parent_pk')))

        try:
            instance.full_clean()
            instance.save()
        except ValidationError as e:
            logger.error(self.request,
                         f"Object creation of {data.get('model_slug')} failed! Check configuration! Error: {e}")
            raise ValidationError(
                f"Object creation of {data.get('model_slug')} failed! Check configuration! Error: {e}")

        logger.info(
            f"{self.request.user} created an instance of {model} ({self.kwargs["nation_slug"]})")

        fields = data.getlist('field_slugs')
        fields_string = ['"' + f + '"' for f in fields]
        fields_string = ', '.join(fields_string)
        tok = self.request.COOKIES.get('csrftoken')
        ans = f"""
        <form class="d-flex" hx-put='{reverse_lazy("b:nation:edit", kwargs={"nation_slug": self.kwargs['nation_slug']})}'
          hx-headers='{{"X-CSRFToken": "{self.request.COOKIES['csrftoken']}"}}'
          hx-vals='{{"field_slugs": [{fields_string}], "model_slug": "{data.get('model_slug')}", "instance_pk": "{instance.pk}"}}'>
            <span class="me-auto my-auto align-middle">
        """
        for field in fields:
            field_value = getattr(instance, field)
            # We're using a protected member correctly, verbose_name is intended to be used in labels
            verbose_name = model._meta.get_field(field).verbose_name
            ans += f'<label class="my-auto" for="{field}">{verbose_name}:</label>\
                           <input type="text" id="{field}" name="{field}" value="{field_value}"> '

        ans += f"""
                        </span>
                        <button class="btn btn-outline-success m-1 hover_darken_content" type="submit">
                            <!-- Uploaded to: SVG Repo, www.svgrepo.com, Generator: SVG Repo Mixer Tools -->
                            <svg fill="#5cb85c" width="17px" height="21px" viewBox="0 4 96 96" xmlns="http://www.w3.org/2000/svg">
                                <title/>
                                <g>
                                    <path d="M58.3945,32.1563,42.9961,50.625l-5.3906-6.4629a5.995,5.995,0,1,0-9.211,7.6758l9.9961,12a5.9914,5.9914,0,0,0,9.211.0059l20.0039-24a5.9988,5.9988,0,1,0-9.211-7.6875Z"/>
                                    <path d="M48,0A48,48,0,1,0,96,48,48.0512,48.0512,0,0,0,48,0Zm0,84A36,36,0,1,1,84,48,36.0393,36.0393,0,0,1,48,84Z"/>
                                </g>
                            </svg>
                        </button>
                        <button class="btn btn-outline-warning m-1 hover_darken_content" type="reset">
                            <!-- Uploaded to: SVG Repo, www.svgrepo.com, Generator: SVG Repo Mixer Tools -->
                            <svg width="17px" height="17px" viewBox="0 1 15 15" fill="none" xmlns="http://www.w3.org/2000/svg">
                              <path
                                fill-rule="evenodd"
                                clip-rule="evenodd"
                                d="M4.85355 2.14645C5.04882 2.34171 5.04882 2.65829 4.85355 2.85355L3.70711 4H9C11.4853 4 13.5 6.01472 13.5 8.5C13.5 10.9853 11.4853 13 9 13H5C4.72386 13 4.5 12.7761 4.5 12.5C4.5 12.2239 4.72386 12 5 12H9C10.933 12 12.5 10.433 12.5 8.5C12.5 6.567 10.933 5 9 5H3.70711L4.85355 6.14645C5.04882 6.34171 5.04882 6.65829 4.85355 6.85355C4.65829 7.04882 4.34171 7.04882 4.14645 6.85355L2.14645 4.85355C1.95118 4.65829 1.95118 4.34171 2.14645 4.14645L4.14645 2.14645C4.34171 1.95118 4.65829 1.95118 4.85355 2.14645Z"
                                fill="#ffc107"
                              />
                            </svg>
                        </button>
                        <button class="btn btn-outline-danger m-1 hover_darken_content"data-bs-toggle="tooltip" data-bs-placement="bottom"
                                data-bs-original-title='Cancel'
                                hx-delete="{reverse_lazy("b:nation:edit", kwargs={"nation_slug": self.kwargs['nation_slug']})}"
                                hx-swap="none">
                            <!-- Uploaded to: SVG Repo, www.svgrepo.com, Generator: SVG Repo Mixer Tools -->
                            <svg fill="#d9534f" width="17px" height="21px" viewBox="0 4 96 96" xmlns="http://www.w3.org/2000/svg">
                                <title/>
                                <g>
                                    <path d="M48,0A48,48,0,1,0,96,48,48.0512,48.0512,0,0,0,48,0Zm0,84A36,36,0,1,1,84,48,36.0393,36.0393,0,0,1,48,84Z"/>
                                    <path d="M64.2422,31.7578a5.9979,5.9979,0,0,0-8.4844,0L48,39.5156l-7.7578-7.7578a5.9994,5.9994,0,0,0-8.4844,8.4844L39.5156,48l-7.7578,7.7578a5.9994,5.9994,0,1,0,8.4844,8.4844L48,56.4844l7.7578,7.7578a5.9994,5.9994,0,0,0,8.4844-8.4844L56.4844,48l7.7578-7.7578A5.9979,5.9979,0,0,0,64.2422,31.7578Z"/>
                                </g>
                            </svg>
                        </button></form> """

        return HttpResponse(ans)

    def delete(self, *args, **kwargs):
        data = QueryDict(self.request.body)
        model = apps.get_model(app_label='Nation', model_name=data.get('model_slug'))
        instance = model.objects.get(pk=data.get('instance_pk'))
        try:
            instance.delete()
        except Exception as e:
            logger.error(e)
            messages.error(self.request, e)
        logger.info(
                f"{self.request.user} deleted {instance.log_info()} -- model {model}, nation ({self.kwargs["nation_slug"]})")
        return HttpResponse("", headers={"HX-Refresh": "true"})
