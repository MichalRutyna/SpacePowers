import random

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http.request import QueryDict
from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls.base import reverse_lazy
from django.views.generic.base import View

from News.models import Roll, Post


# TODO secure all views below this

class RollsPageView(UserPassesTestMixin, View):
    # TODO change into template view?
    template_name = 'news/pages/rolls_page.html'

    errors = []
    def test_func(self):
        # TODO auth
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
            "post": post_object,
        }

        return render(self.request, self.template_name, context)

def make_random_roll():
    return random.randint(1, 20)

class NewRollView(UserPassesTestMixin, View):

    def test_func(self):
        return True

    # roll a present roll
    def put(self, request, *args, **kwargs):
        post = get_object_or_404(Post, slug=self.kwargs['post_slug'])
        data = QueryDict(self.request.body)
        roll = get_object_or_404(Roll, pk=int(data.get('roll_pk')))
        roll.roll = make_random_roll()
        roll.save()
        context = {
            "roll": roll,
            "post": post,
            "roll_pk": roll.pk,
        }
        return render(self.request, "news/parts/components/roll_pills/happy_pill.html", context)

    # create an additional empty roll
    def post(self, *args, **kwargs):
        post = get_object_or_404(Post, slug=self.kwargs['post_slug'])
        if post.rolls.filter(roll_type='success').count() >= settings.MAX_SUCCESS_ROLLS_PER_POST or post.rolls.filter(roll_type='secrecy').count() >= settings.MAX_SECRECY_ROLLS_PER_POST:
            messages.warning(self.request, f"You have reached the current limit of rolls of this type per post. If you need more, please contact an administrator. ")
            return HttpResponse("", headers={"HX-Refresh": "true"})
        roll = Roll(post=post, roll_type=self.kwargs['roll_type'], roll=make_random_roll())
        roll.save()
        context = {
            "roll": roll,
            "post": post,
            "roll_pk": roll.pk,
        }
        return render(self.request, "news/parts/components/roll_pills/happy_pill.html", context)

    # delete an empty roll - not used currently
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
        return render(self.request, "news/parts/components/roll_description_form.html", context)

    def post(self, *args, **kwargs):
        roll = get_object_or_404(Roll, pk=self.kwargs['roll_pk'])
        roll.roll_description = self.request.POST['description']
        roll.save()
        return HttpResponse("<h1 class='text-center text-success'>Saved!</h1>", headers={"HX-Refresh": "true"})

