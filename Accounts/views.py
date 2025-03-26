from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView, \
    PasswordChangeView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView

from django.conf import settings
from .forms import password_reset_form, signup_form, login_form, password_change_form


class ProfileView(TemplateView):
    template_name = "account/profile.html"

    def get_owner_titles(self):
        if self.request.user.is_authenticated:
                ownerships = self.request.user.ownerships.filter(nation__active=True)
                if ownerships:
                    ans = f"Welcome {self.request.user.username}, {ownerships[0].owner_title} of {ownerships[0].nation.name}"
                    for n in range(1, len(ownerships) - 1):
                        nation = ownerships[n]
                        ans += f", {nation.owner_title} of {nation.name}"
                    if ownerships.count() > 1:
                        ans += f" and {ownerships[len(ownerships)-1].owner_title} of {ownerships[len(ownerships)-1].nation.name}"
                    ans += "!"
                    return ans
                else:
                    return "Welcome " + self.request.user.username +"!"
        else:
            return ""

    def get_controlled_nation_count(self):
        if self.request.user.is_authenticated:
            return self.request.user.ownerships.count()
        else:
            return 0

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context.update({"signup_allowed": settings.SIGNUP_ALLOWED,
                        'intro': self.get_owner_titles(),
                        'nation_count': self.get_controlled_nation_count(),
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
