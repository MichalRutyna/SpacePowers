from django.contrib import admin

from .models import Unit, Army

class UnitInLine(admin.TabularInline):
    model = Unit
    extra = 2

class ArmyInLine(admin.TabularInline):
    model = Army
    extra = 0
    fields = ['name', 'slug',]
    inlines = [UnitInLine]

    prepopulated_fields = {'slug': ('name',)}