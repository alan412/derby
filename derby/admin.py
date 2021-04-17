from django.contrib import admin

# Register your models here.
from .models import Group, Car, Heat, Result, Lane


@admin.register(Heat)
class HeatAdmin(admin.ModelAdmin):
    list_display = ('group', 'number')


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('heat', 'lane', 'car', 'time')


@admin.register(Lane)
class LaneAdmin(admin.ModelAdmin):
    list_display = ('number', 'active')


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('name', 'picture', 'owner', 'group', 'number')


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'color')
