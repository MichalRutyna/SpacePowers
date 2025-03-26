from django.contrib import admin

from .models import Unit, Army, Ownership


class UnitInLine(admin.TabularInline):
    model = Unit
    extra = 2

class ArmyInLine(admin.TabularInline):
    model = Army
    extra = 0
    fields = ['name']
    inlines = [UnitInLine]

class OwnershipInLine(admin.TabularInline):
    model = Ownership
    extra = 0
    inlines = [ArmyInLine]