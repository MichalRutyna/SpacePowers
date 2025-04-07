from django.db import models
from django.db.models import Q, FilteredRelation
from django.db.models.aggregates import Count


class NewsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(active=True)

    def published(self):
        posts = self.all().order_by('-created_at')
        return [post for post in posts if post.is_published]

    def unpublished(self):
        posts = self.all().order_by('-created_at')
        return [post for post in posts if not post.is_published]
