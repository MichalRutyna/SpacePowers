from django.urls import path
from django.views.generic.base import TemplateView

from .views import *

app_name = "news"

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('category/<str:slug>/', PostsByCategory.as_view(), name='category'),
    path('tag/<str:slug>/', PostsByTag.as_view(), name='tag'),
    path('post/<str:slug>/', GetPost.as_view(), name='post'),
    path('search/', Search.as_view(), name='search'),
    path('post/<slug:post_id>/add_comment/', add_comment, name='add_comment'),
]
