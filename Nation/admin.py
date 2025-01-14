from django.contrib import admin

from .models import Nation


class NationAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner']

admin.site.register(Nation, NationAdmin)