from django.urls import path

from . import views

urlpatterns = [
    path('', views.main),
    path('register', views.register),
    path('test', views.testHardware),
    path('currentHeat', views.currentHeat),
    path('allCars', views.allCars),
    path('<int:groupId>/start/', views.start),
    path('<int:groupId>/audience/', views.audience),
    path('<int:groupId>/leaderboard/', views.leaderboard),
    path('<int:groupId>/remaining/', views.remainingHeats),
]
