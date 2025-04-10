from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.views.static import serve

from BaseSite.views import markdown_uploader

from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = ([
    path('admin/', admin.site.urls),
    path('martor/', include('martor.urls')),
    path('api/uploader/', markdown_uploader, name='markdown_uploader_page'),
    path('', include("BaseSite.urls", namespace='b')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
   + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))

if settings.DEBUG:
    urlpatterns = [
                      *urlpatterns,
                  ] + debug_toolbar_urls()
