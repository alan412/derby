from django.contrib import admin

# Register your models here.
from .models import Group, Car, Heat, Result

admin.site.register(Group)
admin.site.register(Car)
admin.site.register(Heat)
admin.site.register(Result)
