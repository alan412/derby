from django.urls import path

from . import views

urlpatterns = [
    path('', views.main),
    path('register', views.register),
    path('resetData', views.resetData),
    path('test', views.testHardware),
    path('heatData', views.heatData),
    path('updateHardware', views.updateHardware),
    path('allCars', views.allCars),
    path('fake', views.fake),
    path('<int:groupId>/start/', views.start),
    path('<int:groupId>/rerunLastHeat/', views.rerunLastHeat),
    path('<int:groupId>/audience/', views.audience),
    path('<int:groupId>/leaderboard/', views.leaderboard),
    path('<int:groupId>/allHeats/', views.allHeats),
]
