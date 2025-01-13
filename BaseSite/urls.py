from django.urls import path
from django.urls.conf import include
from django.views.generic.base import TemplateView

app_name = "base"

urlpatterns = [
    path('', TemplateView.as_view(template_name="home.html"), name="home"),
    path('account/', include("Accounts.urls")),
    path('nation/', include('Nation.urls')),
    path('news/', include('News.urls')),
    path('other_nation/', include('OtherNations.urls')),
]