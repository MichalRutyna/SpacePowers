from django.urls import path
from django.urls.conf import include

from .views import HomeView

app_name = "base"

urlpatterns = [
    path('',HomeView.as_view(),name="home"),
    path('account/', include("Accounts.urls")),
    path('nation/', include('Nation.urls')),
    path('news/', include('News.urls')),
    path('foreign_nation/', include('OtherNations.urls')),
    path('map', include('Map.urls')),
]