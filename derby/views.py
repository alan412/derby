from django.shortcuts import render
from django.http import HttpResponse


def register(request):
    context = {}
    return render(request, "derby/register.html", context)

def start(request):
    context = {}
    return render(request, "derby/start.html", context)

def nextHeat(request):
    context = {}
    return render(request, "derby/nextHeat.html", context)

def audience(request):
    context = {}
    return render(request, "derby/audience.html", context)

def currentHeat(request):
    context = {}
    return render(request, "derby/currentHeat.html", context)

def leaderboard(request):
    listCars = [
        {"owner" : "DAD", "name" : "slowpoke", "picture" : "", "speed" : "01:07.02"},
        {"owner" : "Joshua", "name" : "Wabbit","picture" : "Wabbit.jpg", "speed" : "00:42.42"},
        {"owner" : "DAD", "name" : "slowpoke", "picture" : "", "speed" : "01:03.02"},
        {"owner" : "Mom", "name" : "Filthy Panda Stealer", "picture" : "", "speed" : "00:43.02"},
        {"owner" : "Joshua", "name" : "Wabbit","picture" : "Wabbit.jpg", "speed" : "00:49.42"},
        {"owner" : "DAD", "name" : "slowpoke", "picture" : "", "speed" : "01:07.02"},
        {"owner" : "Mom", "name" : "Filthy Panda Stealer", "picture" : "", "speed" : "00:48.02"},
    ]
    context = {"leaderboard" : sorted(listCars, key = lambda car: car['speed'])[:5]}
    return render(request, "derby/leaderboard.html", context)
