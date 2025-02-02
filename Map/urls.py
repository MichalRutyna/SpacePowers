from django.urls.conf import path

from .views import *

app_name = "map"

urlpatterns = [
    path('', MapView.as_view(), name="home"),
]
