from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

from News.models import Post, Comment


@require_POST
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user.is_authenticated:
        if post.liked_by.filter(id=request.user.id).exists():
            post.liked_by.remove(request.user)
        else:
            post.liked_by.add(request.user)
    headers = {
        "HX-Refresh": "true"
    }
    return HttpResponse("", headers=headers)

@require_POST
def like_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user.is_authenticated:
        if comment.liked_by.filter(id=request.user.id).exists():
            comment.liked_by.remove(request.user)
        else:
            comment.liked_by.add(request.user)
    headers = {
        "HX-Refresh": "true"
    }
    return HttpResponse("", headers=headers)