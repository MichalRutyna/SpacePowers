from django.views.generic.list import ListView

from .models import *

class MapView(ListView):
    model = Region
    template_name = 'map/home.html'
    paginate_by = None


