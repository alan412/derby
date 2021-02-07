from django.contrib import admin

# Register your models here.
from .models import Group, Car, Heat, Result

admin.site.register(Heat)
admin.site.register(Result)


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('name', 'picture', 'owner', 'group', 'number')


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'color')
