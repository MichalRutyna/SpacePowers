from django.conf import settings
from django.urls.base import reverse_lazy

from Nation.models import Nation


def get_nation_dropdown(request):
    if request.user.is_authenticated:
        nations = Nation.objects.filter(active=True)
        response = ""

        response += '<a class="nav-link dropdown-toggle" data-bs-toggle="dropdown" role="button"\
                        aria-haspopup="true" aria-expanded="false">Other nations</a>\
                    <div class="dropdown-menu">'

        for nation in nations:
            url = reverse_lazy('b:other_nations:nation_details', args=(nation.slug,))
            name = nation.name

            response += f"<a class='dropdown-item' href='{url}'>{name}</a>"
        summary_url = reverse_lazy('b:other_nations:summary')
        # response += f'<div class="dropdown-divider"></div>\
        #             <a class="dropdown-item" href="{summary_url}">Summary</a></div>'

        return {'dropdown': response}
    else:
        return {}

def get_settings_context(request):
    return {'moderation_post_nation': settings.MODERATOR_POST_NATION}