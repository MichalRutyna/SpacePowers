from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView


class SignUpView(CreateView):
    form_class = UserCreationForm
    # user has to login after registration
    success_url = reverse_lazy("b:account:login")
    template_name = "registration/signup.html"

class LoginView(LoginView):
    form_class = AuthenticationForm
    success_url = reverse_lazy("b:account:home")
    template_name = "registration/login.html"