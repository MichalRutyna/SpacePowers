from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models.aggregates import Count
from django.http.request import QueryDict
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
from .forms import CommentForm, PostForm, RollsForm
from .models import Post, Category, Tag, Comment, Roll
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

        comments = Comment.objects.annotate(cc=Count("liked_by")).filter(post=self.object, is_published=True).order_by('-cc')
        paginator = Paginator(comments, 100)
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

        return render(self.request, '403.html', context)

    def form_valid(self, form):
        form.instance.slug = slugify(form.cleaned_data['title'])
        form.instance.author = self.request.user
        form.instance.category = get_object_or_404(Category, slug=settings.CURRENT_CATEGORY_SLUG)
        x = super().form_valid(form)
        if self.object.requires_success_roll():
            Roll(post=self.object, roll_type='success').save()
        if self.object.requires_secrecy_roll():
            Roll(post=self.object, roll_type='secrecy').save()
        return x

# TODO secure all views below this

class AddRollView(UserPassesTestMixin, View):
    # TODO change into template view?
    template_name = 'news/pages/add_roll.html'

    errors = []
    def test_func(self):
        return True

    def get(self, *args, **kwargs):
        post_slug = self.kwargs['post_slug']
        post_object = get_object_or_404(Post, slug=post_slug)
        success_url = reverse_lazy("b:news:post", kwargs={'slug': post_slug})
        context = {
            "success_roll_required": post_object.requires_success_roll(),
            "secret_roll_required": post_object.requires_secrecy_roll(),
            "success_rolls": post_object.get_success_rolls(),
            "secrecy_rolls": post_object.get_secrecy_rolls(),
            "has_unrolled": post_object.has_unrolled_rolls(),
            "post_slug": post_slug,
            "post_title": post_object.title,
        }

        return render(self.request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        print(request.POST)
        # TODO handle post
        return HttpResponse("")

def make_random_roll():
    return random.randint(1, 20)

class NewRollView(UserPassesTestMixin, View):

    def test_func(self):
        return True

    # create an additional empty roll
    def post(self, *args, **kwargs):
        post = get_object_or_404(Post, slug=self.kwargs['post_slug'])
        if post.rolls.filter(roll_type='success').count() >= settings.MAX_SUCCESS_ROLLS_PER_POST or post.rolls.filter(roll_type='secrecy').count() >= settings.MAX_SECRECY_ROLLS_PER_POST:
            messages.warning(self.request, f"You have reached the current limit of rolls per post of {settings.MAX_ROLLS_PER_POST}. If you still need more, please contact an administrator. ")
            return HttpResponse("", headers={"HX-Refresh": "true"})
        roll = Roll(post=post, roll_type=self.kwargs['roll_type'], roll=make_random_roll())
        roll.save()
        context = {
            "roll": roll,
            "post_slug": post.slug,
            "roll_pk": roll.pk,
        }
        return render(self.request, "news/parts/components/roll_pills/happy_pill.html", context)
    # delete an empty roll
    def delete(self, *args, **kwargs):
        pk = QueryDict(self.request.body).get('pk', None)
        post = get_object_or_404(Post, slug=self.kwargs['post_slug'])
        roll = get_object_or_404(Roll, pk=pk)\

        if (post.roll_type == "success" and post.requires_success_roll() and post.rolls.filter(roll_type=roll.roll_type).count() == 1) or \
            (post.roll_type == "secrecy" and post.requires_secrecy_roll() and post.rolls.filter(roll_type=roll.roll_type).count() == 1):
            messages.warning(self.request,
                             f"This roll cannot be deleted. This post specifically requires at least one roll of this type.")
            return HttpResponse("", headers={"HX-Refresh": "true"})

        roll.delete()


class DescriptionView(UserPassesTestMixin, View):
    def test_func(self):
        return True

    def get(self, *args, **kwargs):
        context = {
            'post_slug': self.kwargs['post_slug'],
            'roll': get_object_or_404(Roll, pk=self.kwargs['roll_pk']),
        }
        return render(self.request, "news/parts/roll_description_form.html", context)

    def post(self, *args, **kwargs):
        roll = get_object_or_404(Roll, pk=self.kwargs['roll_pk'])
        roll.roll_description = self.request.POST['description']
        roll.save()
        return HttpResponse("")
