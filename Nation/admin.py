from django.contrib import admin

from .models import Nation, Army
from .admin_inlines import *


class NationAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner']
    inlines = [ArmyInLine]

class ArmyAdmin(admin.ModelAdmin):
    list_display = ['name', 'nation']
    inlines = [UnitInLine]


admin.site.register(Nation, NationAdmin)
admin.site.register(Army, ArmyAdmin)