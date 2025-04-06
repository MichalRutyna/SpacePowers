from django.shortcuts import get_list_or_404
from django.urls.base import reverse_lazy
from django.views.generic.list import ListView

from News.models import Post


class UnpublishedListView(ListView):
    template_name = "news/pages/not_published.html"
    context_object_name = 'posts'
    paginate_by = 10
    allow_empty = True

    def get_queryset(self):
        queryset = Post.objects.filter(is_published=False, author=self.request.user).order_by('-created_at')
        for obj in queryset:
            if obj.has_unrolled_rolls():
                obj.unpublished_reason = f"Missing a required roll <a href='{reverse_lazy("b:news:rolls_page", kwargs={"post_slug":obj.slug})}' class='btn btn-info'>Fix</a>"
            elif obj.has_rolls_without_description():
                obj.unpublished_reason = f"A roll is missing description <a href='{reverse_lazy("b:news:rolls_page", kwargs={"post_slug":obj.slug})}' class='btn btn-info'>Fix</a>"
            else:
                obj.unpublished_reason = "Waits for moderation's approval"
        return queryset