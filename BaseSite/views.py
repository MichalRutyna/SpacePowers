from django.shortcuts import render
from django.views.generic.base import View

from News.models import Post
from Nation.models import Nation

class HomeView(View):
    def get_context_data(self, *, object_list=None, **kwargs):
        context = {}
        pinned_post = Post.objects.latest('created_at')
        pinned_post.save()
        pinned_post.refresh_from_db()
        context['pinned_post'] = pinned_post

        nations = Nation.objects.all()
        latest_posts_by_nation = {}
        for nation in nations:
            latest_posts_by_nation[nation.slug] = Post.objects.filter(nation=nation)[:2]

        context['latest_posts_by_nation'] = latest_posts_by_nation
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        template = 'home.html'
        return render(request, template, context)