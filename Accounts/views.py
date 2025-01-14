from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView, \
    PasswordChangeView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import password_reset_form, signup_form, login_form, password_change_form

# log out
class SignUpView(CreateView):
    # user has to log in after registration
    form_class =  signup_form.CreateUserForm
    success_url = reverse_lazy("b:account:login")
    template_name = "registration/signup.html"

# log in
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
