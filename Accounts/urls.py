from django.contrib.auth.views import PasswordResetCompleteView, PasswordResetDoneView, PasswordChangeDoneView, LogoutView
from django.urls import path

from .views import *
app_name = "account"

urlpatterns = [
    path('', ProfileView.as_view(), name="home"),
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
