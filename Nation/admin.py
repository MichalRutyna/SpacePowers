from django.contrib import admin

from .models import Nation, Army
from .admin_inlines import *


class NationAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner']
    prepopulated_fields = {'slug':('name',)}
    inlines = [ArmyInLine]

class ArmyAdmin(admin.ModelAdmin):
    list_display = ['name', 'nation']
    prepopulated_fields = {'slug':('name',)}
    inlines = [UnitInLine]


admin.site.register(Nation, NationAdmin)
admin.site.register(Army, ArmyAdmin)