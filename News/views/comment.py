from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST

from News.models import Comment, Post


@require_POST
def add_comment(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    username = request.user.username
    nation = request.user.claimed_nations.first()
    comment_text = request.POST.get('comment')

    comment_valid = len(comment_text) >= 2 and all(c.isalnum() or c in ',.-_!?\' ' for c in comment_text)

    if not comment_valid:
        response_data = {
            "success": False,
            "errors": {
                'comment': 'Invalid input' if not comment_valid else '',
            },
        }
        return redirect("b:news:post", slug=post_slug, response=response_data)

    comment = Comment(author=request.user, comment=comment_text, nation=nation, post=post)
    comment.save()

    return redirect("b:news:post", slug=post_slug)