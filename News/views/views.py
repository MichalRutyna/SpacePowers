from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.paginator import Paginator
from django.db.models import F
from django.db.models.aggregates import Count
from django.shortcuts import render, get_object_or_404
from django.template.defaultfilters import slugify
from django.urls.base import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView

from News.forms import CommentForm, PostForm, PostEditForm
from News.models import Post, Category, Comment, Roll


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

    # TODO if unpublished check if user is the author

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object.views = F('views') + 1
        if self.request.user.is_authenticated:
            if self.request.user.id not in self.object.seen_by.all():
                self.object.seen_by.add(self.request.user)
        self.object.save()
        self.object.refresh_from_db()

        context['viewed_by_author'] = self.object.is_user_an_author(self.request.user)

        comments = Comment.objects.annotate(cc=Count("liked_by")).filter(post=self.object, is_published=True).order_by(
            '-cc')
        paginator = Paginator(comments, 100)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['comments'] = page_obj

        context['comment_form'] = CommentForm(user=self.request.user)
        return context


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


class EditPostView(UserPassesTestMixin, UpdateView):
    model = Post
    template_name = "news/pages/edit_post.html"
    form_class = PostEditForm

    errors = []

    def test_func(self):
        allowed = True
        if not settings.POST_CREATION_ALLOWED:
            allowed = False
            self.errors.append('An administrator has disabled post edition.')
        if not self.request.user.has_perm('News.change_post'):
            allowed = False
            self.errors.append('You do not have the permissions!')

        if not self.get_object().is_user_an_author(self.request.user):
            allowed = False
            self.errors.append('You are not the author of this post!')
        return allowed

    def handle_no_permission(self):
        context = {"error": "forbidden",
                   "message": "You cannot edit this post:<br>" + self.errors[0]}

        return render(self.request, '403.html', context)
