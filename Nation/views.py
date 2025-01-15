from django.shortcuts import render
from django.views.generic.base import View

from .models import Nation

class NationHomeView(View):
    success_template = 'nation/home.html'
    missing_nation_template = 'nation/no_nation.html'

    def get(self, request):
        context = {}
        try:
            nation = Nation.objects.get(owner_id=request.user.id)
            context['nation'] = nation
        except Nation.DoesNotExist as e:
            pass

        return render(request, self.success_template, context)

# TODO tworzenie państwa