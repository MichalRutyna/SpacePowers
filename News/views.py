from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView

from .forms import CommentForm
from .models import Post, Category, Tag, Comment
from Nation.models import Nation

from django.db.models import F
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404


class Home(ListView):
    model = Post
    template_name = 'news/home.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_queryset(self):
        return Post.objects.order_by('-created_at')


class PostsByCategory(ListView):
    template_name = 'news/category.html'
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
        context['title'] = Category.objects.get(slug=self.kwargs['slug'])
        return context


class PostsByNation(ListView):
    template_name = 'news/nation.html'
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
        context['title'] = Nation.objects.get(slug=self.kwargs['slug'])
        return context


class GetPost(DetailView):
    model = Post
    template_name = 'news/single.html'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object.views = F('views') + 1
        if self.request.user.id not in self.object.seen_by.all():
            self.object.seen_by.add(self.request.user)
        self.object.save()
        self.object.refresh_from_db()

        comments = Comment.objects.filter(post=self.object, is_published=True).order_by('-created_at')
        paginator = Paginator(comments, 5)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['comments'] = page_obj

        context['form'] = CommentForm()
        return context


class PostsByTag(ListView):
    template_name = 'news/tag.html'
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


class PostsByAuthor(ListView):
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
    template_name = 'news/search.html'
    context_object_name = 'posts'
    paginate_by = 4

    def get_queryset(self):
        return Post.objects.filter(title__icontains=self.request.GET.get('s'))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('s')
        return context


@csrf_protect
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
        #return JsonResponse(response_data)
        return redirect("b:news:post", slug=post_slug)

    comment = Comment(author=request.user, comment=comment_text, nation=nation, post=post)
    comment.save()

    response_data = {
        'success': True,
        'author': comment.author.id,
        'created_at': comment.created_at.strftime('%d %B %Y'),
        'comment': comment.comment,
    }
    return redirect("b:news:post", slug=post_slug)