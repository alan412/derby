import re
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
from derby.forms import RegisterForm, SelectGroupForm
from derby.models import Car, Group
from derby.generateHeats import generateHeats
from derby.getTimes import getTimes


def groupFromId(groupId):
    return Group.objects.get(id=groupId)


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            # process data
            car = form.save(commit=False)
            car.assignNumber()
            car.save()
            context = {"color": car.group.color,
                       "imglink": car.picture,
                       "owner": car.owner,
                       "name": car.name,
                       "group": car.group.name,
                       "number": car.number}

            return render(request, "derby/registered.html", context)
    else:
        form = RegisterForm()
    context = {'form': form}
    return render(request, "derby/register.html", context)


def main(request):
    context = {'form': SelectGroupForm()}
    return render(request, "derby/main.html", context)


def start(request, groupId):
    generateHeats(groupFromId(groupId))
    return audience(request, groupId)


def audience(request, groupId):
    template = request.GET.get('next', 'derby/leaderboard.html')

    if template == 'derby/leaderboard.html':
        context = {"timeout": 10_000, "audience": True,
                   "next": "derby/nextHeat.html"}
        return showLeaderboard(request, context, groupId)
    else:
        context = {}

    return render(request, template, context)


def currentHeat(request):
    context = {}
    return render(request, "derby/currentHeat.html", context)


def remainingHeats(request, group):
    # needs to be changed to be the color of the group
    context = {"color": "red"}
    return render(request, "derby/remaining.html", context)


def allCars(request):
    context = {"cars": Car.objects.all()}
    return render(request, "derby/allCars.html", context)


def showLeaderboard(request, context, groupId):
    group = Group.objects.get(id=groupId)
    context["cars"] = getTimes(group)
    context["group"] = group
    return render(request, "derby/leaderboard.html", context)


def leaderboard(request, groupId):
    context = {}
    return showLeaderboard(request, context, groupId)
