from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import *

app_name = "news"

urlpatterns = [
    path('',Home.as_view(), name='home'),
    path('create_post/', login_required(AddPostView.as_view()), name='create_post'),
    path('edit_post/<slug:slug>', login_required(EditPostView.as_view()), name='edit_post'),

    # Likes and comments
    path('post/like/<int:pk>/', login_required(like_post), name='like_post'),
    path('comment/like/<int:pk>/', login_required(like_comment), name='like_comment'),
    path('post/<slug:post_slug>/add_comment/', login_required(add_comment), name='add_comment'),

    # Filters
    path('category/<str:slug>/',PostsByCategory.as_view(), name='category'),
    path('from_arc/<str:slug>/',PostsByArc.as_view(), name='arc'),
    path('nation/<str:slug>/',PostsByNation.as_view(), name='nation'),
    path('tag/<str:slug>/', PostsByTag.as_view(), name='tag'),
    path('author/<int:pk>/', PostsByAuthor.as_view(), name='author'),
    path('search/',Search.as_view(), name='search'),

    path('unpublished/', login_required(UnpublishedListView.as_view()), name='unpublished'),
    path('post/<str:post_slug>/rolls', login_required(RollsPageView.as_view()), name='rolls_page'),
    path('arcs/', login_required(ArcsPageView.as_view()), name='arcs_page'),

    # Rolls api
    path('post/<str:post_slug>/new_roll/<str:roll_type>', login_required(NewRollView.as_view()), name='new_roll'),
    path('post/<str:post_slug>/roll/<int:roll_pk>/description', login_required(DescriptionView.as_view()), name='description'),

    # Arcs api
    path('arcs/new_arc', login_required(ArcAddAPI.as_view()), name='new_arc'),
    path('arcs/<str:slug>', login_required(ArcManageAPI.as_view()), name='arc_details'),

    path('post/<str:slug>/', GetPost.as_view(), name='post'),
]
