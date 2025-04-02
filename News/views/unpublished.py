from django.shortcuts import get_list_or_404
from django.views.generic.list import ListView

from News.models import Post


class UnpublishedListView(ListView):
    template_name = "news/pages/not_published.html"
    context_object_name = 'posts'
    paginate_by = 10
    allow_empty = True
    queryset = Post.objects.filter(is_published=False)
