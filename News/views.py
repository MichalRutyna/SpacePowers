from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.http.response import HttpResponse
from django.template.defaultfilters import slugify
from django.urls.base import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from django.views.generic.edit import CreateView

from django.conf import settings
from .forms import CommentForm, PostForm
from .models import Post, Category, Tag, Comment
from Nation.models import Nation

from django.db.models import F
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404

import random


class Home(ListView):
    model = Post
    template_name = 'news/pages/home.html'
    context_object_name = 'posts'
    paginate_by = 2

    extra_context = {'post_creation_allowed': settings.POST_CREATION_ALLOWED}

    def get_queryset(self):
        return Post.objects.order_by('-created_at')


class GetPost(DetailView):
    model = Post
    template_name = 'news/pages/single.html'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object.views = F('views') + 1
        if self.request.user.is_authenticated:
            if self.request.user.id not in self.object.seen_by.all():
                self.object.seen_by.add(self.request.user)
        self.object.save()
        self.object.refresh_from_db()

        comments = Comment.objects.filter(post=self.object, is_published=True).order_by('-liked_by')
        paginator = Paginator(comments, 5)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['comments'] = page_obj

        context['comment_form'] = CommentForm(user=self.request.user)
        return context


class PostsByCategory(ListView):
    template_name = 'news/pages/sort_by/category.html'
    context_object_name = 'posts'
    paginate_by = 10
    allow_empty = False

    def get_queryset(self):
        queryset = Post.objects.filter(category__slug=self.kwargs['slug']).order_by('-created_at')
        if not queryset.exists():
            raise Http404("No posts found in this category.")
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.get(slug=self.kwargs['slug'])
        return context


class PostsByNation(ListView):
    template_name = 'news/pages/sort_by/nation.html'
    context_object_name = 'posts'
    paginate_by = 4
    allow_empty = False

    def get_queryset(self):
        queryset = Post.objects.filter(nation__slug=self.kwargs['slug']).order_by('-created_at')
        if not queryset.exists():
            raise Http404("No posts found from this nation.")
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nation'] = Nation.objects.get(slug=self.kwargs['slug'])
        return context


class PostsByTag(ListView):
    template_name = 'news/pages/sort_by/tag.html'
    context_object_name = 'posts'
    paginate_by = 4
    allow_empty = False

    def get_queryset(self):
        queryset = Post.objects.filter(tags__slug=self.kwargs['slug']).order_by('-created_at')
        if not queryset.exists():
            raise Http404("No posts found with this tag.")
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag_object'] = Tag.objects.get(slug=self.kwargs['slug'])
        return context


class PostsByAuthor(View):
    template_name = 'news/author.html'
    context_object_name = 'posts'
    paginate_by = 4
    allow_empty = False

    def get_queryset(self):
        queryset = Post.objects.filter(author__id=self.kwargs['pk']).order_by('-created_at')
        if not queryset.exists():
            raise Http404("No posts found from this author.")
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = User.objects.get(id=self.kwargs['pk'])
        return context


class Search(ListView):
    template_name = 'news/pages/sort_by/search.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        return Post.objects.filter(title__icontains=self.request.GET.get('s'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('s')
        return context


def like_post(request, pk):
    if request.method == 'POST':
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

def like_comment(request, pk):
    if request.method == 'POST':
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


@csrf_protect
@require_POST
@login_required
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
        return redirect("b:news:post", slug=post_slug)

    comment = Comment(author=request.user, comment=comment_text, nation=nation, post=post)
    comment.save()

    return redirect("b:news:post", slug=post_slug)


@method_decorator(csrf_protect, name='dispatch')
@method_decorator(login_required, name='dispatch')
class AddPostView(UserPassesTestMixin, CreateView):
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    form_class = PostForm
    template_name = 'news/pages/create_post.html'
    success_url = reverse_lazy("b:news:home")

    errors = []

    def test_func(self):
        allowed = True
        if not settings.POST_CREATION_ALLOWED:
            allowed = False
            self.errors.append('An administrator has disabled post creation.')
        if not self.request.user.has_perm('News.add_post'):
            allowed = False
            self.errors.append('You do not have the permissions!')
        return allowed

    def handle_no_permission(self):
        context = {"error": "forbidden",
                   "message": "You cannot create a post!<br>" + self.errors[0]}

        return render(self.request, 'errors/forbidden.html', context)

    def form_valid(self, form):
        form.instance.slug = slugify(form.cleaned_data['title'])
        form.instance.author = self.request.user
        form.instance.category = Category.objects.get(slug=settings.CURRENT_CATEGORY_SLUG)
        form.instance.roll = random.randint(1, 20)
        return super().form_valid(form)
