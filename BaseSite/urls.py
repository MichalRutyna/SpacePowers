from django.urls import path
from django.urls.conf import include
from django.views.generic.base import TemplateView

from .views import HomeView

app_name = "base"

urlpatterns = [
    path('',HomeView.as_view(),name="home"),
    path('account/', include("Accounts.urls")),
    path('nation/', include('Nation.urls')),
    path('news/', include('News.urls')),
    path('other_nation/', include('OtherNations.urls')),
]