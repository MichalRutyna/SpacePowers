from django.urls.base import reverse_lazy
from django.views.generic.list import ListView

from News.models import Post


class UnpublishedListView(ListView):
    template_name = "news/pages/not_published.html"
    context_object_name = 'posts'
    paginate_by = 10
    allow_empty = True

    def get_queryset(self):
        posts = Post.active_posts.unpublished()
        posts = [post for post in posts if post.is_user_an_author(self.request.user)]
        for post in posts:
            if post.has_unrolled_rolls():
                post.unpublished_reason = f"Missing a required roll <a href='{reverse_lazy("b:news:rolls_page", kwargs={"post_slug":post.slug})}' class='btn btn-info'>Fix</a>"
            elif post.has_rolls_without_description():
                post.unpublished_reason = f"A roll is missing description <a href='{reverse_lazy("b:news:rolls_page", kwargs={"post_slug":post.slug})}' class='btn btn-info'>Fix</a>"
            elif post.published_override is not None:
                post.unpublished_reason = f"A moderator has unpublished your post. Please contact them"
            elif not post.published_by_user:
                post.unpublished_reason = f"You have not yet published this post <a href='{reverse_lazy("b:news:post", kwargs={"slug":post.slug})}' class='btn btn-info'>Fix</a>"
            elif not post.approved_by_admin:
                post.unpublished_reason = f"Your post waits for a moderator's approval"
            else:
                post.unpublished_reason = "Ann error has occurred. Please contact the administrator"
        return posts