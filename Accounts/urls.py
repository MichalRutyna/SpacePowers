from django.contrib.auth.views import PasswordResetCompleteView, PasswordResetDoneView, PasswordChangeDoneView, LogoutView
from django.urls import path
from django.urls.base import reverse_lazy
from django.urls.conf import include
from django.views.generic.base import TemplateView

from .views import SignUpView, CustomLoginView, CustomPasswordResetView, CustomPasswordChangeView, CustomResetPassConfirmView

app_name = "account"

urlpatterns = [
    path('', TemplateView.as_view(template_name="account/profile.html"), name="home"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("password_reset/", CustomPasswordResetView.as_view(), name="password_reset"),
    path("reset/<uidb64>/<token>/", CustomResetPassConfirmView.as_view(), name="password_reset_confirm"),
    path("password_reset/done/", PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/done/", PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path("password_change/", CustomPasswordChangeView.as_view(), name="password_change"),
    path("password_change/done/", PasswordChangeDoneView.as_view(), name="password_change_done"),
]
