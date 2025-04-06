from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView, \
    PasswordChangeView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http.response import HttpResponse
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView

from django.conf import settings

from Nation.models import get_user_nations
from .forms import password_reset_form, signup_form, login_form, password_change_form


class ProfileView(UserPassesTestMixin, TemplateView):
    template_name = "account/home_profile.html"
    not_owner_template_name = "account/profile.html"
    no_account_template_name = "account/no_account.html"

    def test_func(self):
        return self.request.user.is_authenticated

    def handle_no_permission(self):
        context = {
            "signup_allowed": settings.SIGNUP_ALLOWED,
        }
        return render(self.request, "account/no_account.html", context)

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            if username := self.kwargs.get("username"):
                self.requested_user = get_object_or_404(User, username=username)
            else :
                self.requested_user = self.request.user
            self.is_owner = self.requested_user == self.request.user
            if not self.is_owner:
                self.template_name = self.not_owner_template_name
        else:
            self.template_name = self.no_account_template_name
        return super().dispatch(request, *args, **kwargs)

    def get_owner_titles(self):
        ownerships =self.requested_user.ownerships.filter(nation__active=True)
        if ownerships:
            # ans = f"Welcome {self.request.user.username}, {ownerships[0].owner_title} of {ownerships[0].nation.name}"
            titles = f", {ownerships[0].owner_title} of {ownerships[0].nation.name}"
            for n in range(1, len(ownerships) - 1):
                nation = ownerships[n]
                titles += f", {nation.owner_title} of {nation.name}"
            if ownerships.count() > 1:
                titles += f" and {ownerships[len(ownerships)-1].owner_title} of {ownerships[len(ownerships)-1].nation.name}"
        else:
            titles = ""

        if self.is_owner:
            return f"Welcome {self.requested_user.username}{titles}!"
        else:
            return f"Out information about {self.requested_user.username}{titles}:"

    def get_controlled_nation_count(self):
        return self.requested_user.ownerships.count()

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context.update({"signup_allowed": settings.SIGNUP_ALLOWED,
                        'intro': self.get_owner_titles(),
                        'nation_count': self.get_controlled_nation_count(),
                        'nations': get_user_nations(self.requested_user),
                        'max_nation_count': settings.MAX_NATIONS_PER_USER,
                        'nation_creation_allowed': settings.NATION_CREATION_ALLOWED,
                        })
        return context


class SignUpView(UserPassesTestMixin, CreateView):
    form_class = signup_form.CreateUserForm
    template_name = "registration/signup.html"
    # user has to log in after registration
    success_url = reverse_lazy("b:account:login")

    def test_func(self):
        return settings.SIGNUP_ALLOWED


class CustomLoginView(LoginView):
    form_class = login_form.LoginForm
    success_url = reverse_lazy("b:account:home")


# enter old and new password
class CustomPasswordChangeView(PasswordChangeView):
    form_class = password_change_form.PasswordChangeFormCustom
    success_url = reverse_lazy("b:account:password_change_done")


# enter email to reset password
class CustomPasswordResetView(PasswordResetView):
    form_class = password_reset_form.PasswordResetFormCustom
    success_url = reverse_lazy("b:account:password_reset_done")


# enter new password
class CustomResetPassConfirmView(PasswordResetConfirmView):
    form_class = password_reset_form.SetPasswordFormCustom
    success_url = reverse_lazy("b:account:password_reset_complete")
