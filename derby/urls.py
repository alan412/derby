from django.urls import path

from . import views

urlpatterns = [
    path('', views.main),
    path('register', views.register),
    path('audience', views.audience),
    path('currentHeat', views.currentHeat),
    path('leaderboard', views.leaderboard),
    path('nextHeat', views.nextHeat),
    path('start', views.start)
]
