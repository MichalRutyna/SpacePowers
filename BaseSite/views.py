from django.shortcuts import render
from django.views.generic.base import View

from News.models import Post
from Nation.models import Nation

class HomeView(View):
    def get_context_data(self, *, object_list=None, **kwargs):
        context = {}
        pinned_post = None
        try:
            pinned_post = Post.objects.latest('created_at')
        except Post.DoesNotExist:
            pass
        context['pinned_post'] = pinned_post

        nations = Nation.objects.all()
        latest_posts_by_nation = {}
        for nation in nations:
            latest_posts_by_nation[nation.name] = Post.objects.filter(nation=nation)[:2]

        context['latest_posts_by_nation'] = latest_posts_by_nation
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        template = 'home.html'
        return render(request, template, context)


import os
import json
import uuid

from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from martor.utils import LazyEncoder


@login_required
def markdown_uploader(request):
    """
    Makdown image upload for locale storage
    and represent as json to markdown editor.
    """
    if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        if 'markdown-image-upload' in request.FILES:
            image = request.FILES['markdown-image-upload']
            image_types = [
                'image/png', 'image/jpg',
                'image/jpeg', 'image/pjpeg', 'image/gif'
            ]
            if image.content_type not in image_types:
                data = json.dumps({
                    'status': 405,
                    'error': 'Bad image format.'
                }, cls=LazyEncoder)
                return HttpResponse(
                    data, content_type='application/json', status=405)

            if image.size > settings.MAX_IMAGE_UPLOAD_SIZE:
                to_MB = settings.MAX_IMAGE_UPLOAD_SIZE / (1024 * 1024)
                data = json.dumps({
                    'status': 405,
                    'error': 'Maximum image file is %(size)s MB.' % {'size': to_MB}
                }, cls=LazyEncoder)
                return HttpResponse(
                    data, content_type='application/json', status=405)

            img_uuid = "{0}-{1}".format(uuid.uuid4().hex[:10], image.name.replace(' ', '-'))
            tmp_file = os.path.join(settings.MARTOR_UPLOAD_PATH, img_uuid)
            def_path = default_storage.save(tmp_file, ContentFile(image.read()))
            img_url = os.path.join(settings.MEDIA_URL, def_path)

            data = json.dumps({
                'status': 200,
                'link': img_url,
                'name': image.name
            })
            return HttpResponse(data, content_type='application/json')
        return HttpResponse('Invalid request!')
    return HttpResponse('Invalid request!')