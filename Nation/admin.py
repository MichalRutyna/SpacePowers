from django.contrib import admin

from .models import Nation


class NationAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner']
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Nation, NationAdmin)