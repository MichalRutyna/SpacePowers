from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from Nation.models import Nation


class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, verbose_name='Category_url', unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={"slug": self.slug})

    class Meta:
        verbose_name = 'Category(s)'
        verbose_name_plural = 'Categories'
        ordering = ['title']


class Tag(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, verbose_name='Slug_url', unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('b:news:tag', kwargs={"slug": self.slug})

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
        ordering = ['title']


class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name='Name')
    slug = models.SlugField(max_length=255, unique=True, verbose_name='Link')
    author = models.ForeignKey(User, on_delete=models.PROTECT, null=True, verbose_name='Author')
    nation = models.ForeignKey(Nation, on_delete=models.PROTECT, null=True, verbose_name='Nation')
    content = models.TextField(blank=True, verbose_name='Content')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Published')
    views = models.IntegerField(default=0, verbose_name='Number of views')
    seen_by = models.ManyToManyField(User, blank=True, verbose_name='Seen by', related_name='+')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='posts', verbose_name='Category')
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts', verbose_name='Tag')
    roll = models.IntegerField(default=-1, verbose_name='Roll')
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('b:news:post', kwargs={"slug": self.slug})

    class Meta:
        verbose_name = 'Article(s)'
        verbose_name_plural = 'Articles'
        ordering = ['-created_at']


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', related_query_name='comments', verbose_name='Post')
    author = models.ForeignKey(User, on_delete=models.PROTECT, null=True, verbose_name='Author')
    nation = models.ForeignKey(Nation, on_delete=models.PROTECT, null=True, verbose_name='Nation')
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)
    metagame = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.author} commented: {self.comment}"