from django.conf import settings
from django.conf.urls.static import static
from django.urls.conf import path
from django.views.generic.base import TemplateView

from .views import *

app_name = "map"

urlpatterns = [
    path('', MapView.as_view(), name="home"),
] + static(settings.UPLOAD_URL, document_root=settings.UPLOAD_ROOT)
