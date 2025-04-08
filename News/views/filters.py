from django.contrib.auth.models import User
from django.http.response import Http404
from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView

import settings
from News.models import Post, Tag, Category, Arc
from Nation.models import Nation


class PostsByCategory(ListView):
    template_name = 'news/pages/sort_by/category.html'
    context_object_name = 'posts'
    paginate_by = 10
    allow_empty = True

    def get_queryset(self):
        queryset = Post.objects.filter(category__slug=self.kwargs['slug']).order_by('-created_at')
        if not queryset.exists():
            raise Http404("No posts found in this category.")
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(Category, slug=self.kwargs['slug'])

        return context

class PostsByArc(ListView):
    template_name = 'news/pages/sort_by/arc.html'
    context_object_name = 'posts'
    paginate_by = 10
    allow_empty = True

    def get_queryset(self):
        return [p for p in Post.active_posts.published() if p.arcs.exists() and p.arcs.filter(slug=self.kwargs['slug']).exists()]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['arc'] = get_object_or_404(Arc, slug=self.kwargs['slug'])

        return context


class PostsByNation(ListView):
    template_name = 'news/pages/sort_by/nation.html'
    context_object_name = 'posts'
    paginate_by = 10
    allow_empty = True

    def get_queryset(self):
        if self.kwargs['slug'] == settings.MODERATOR_POST_NATION:
            return [p for p in Post.active_posts.published() if not p.nation]
        return [p for p in Post.active_posts.published() if p.nation and p.nation.slug == self.kwargs['slug']]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.kwargs['slug'] == settings.MODERATOR_POST_NATION:
            context['nation'] =  settings.MODERATOR_POST_NATION
        else:
            context['nation'] = get_object_or_404(Nation, slug=self.kwargs['slug'])
        return context


class PostsByTag(ListView):
    template_name = 'news/pages/sort_by/tag.html'
    context_object_name = 'posts'
    paginate_by = 10
    allow_empty = True

    def get_queryset(self):
        return [p for p in Post.active_posts.published() if p.tags.exists() and p.tags.filter(slug=self.kwargs['slug']).exists()]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag_object'] = Tag.objects.get(slug=self.kwargs['slug'])
        return context


class PostsByAuthor(ListView):
    template_name = 'news/pages/sort_by/author.html'
    context_object_name = 'posts'
    paginate_by = 4
    allow_empty = True

    def get_queryset(self):
        return [p for p in Post.active_posts.published() if p.author and p.author.pk == self.kwargs['pk']]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = User.objects.get(id=self.kwargs['pk'])
        return context


class Search(ListView):
    template_name = 'news/pages/sort_by/search.html'
    context_object_name = 'posts'
    paginate_by = 4
    allow_empty = True

    def get_queryset(self):
        return [p for p in Post.active_posts.published() if p.title and self.request.GET.get('s') in p.title]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('s')
        return context

