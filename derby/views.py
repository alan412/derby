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
    context = {}
    return render(request, "derby/leaderboard.html", context)
