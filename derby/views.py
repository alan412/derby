from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
from derby.forms import RegisterForm, SelectGroupForm
from derby.models import Car, Group
from derby.generateHeats import generateHeats
from derby.getTimes import getTimes


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


def start(request):
    # needs to change to which group is being started
    groups = Group.objects.all()
    for group in groups:
        generateHeats(group)
    context = {}
    return render(request, "derby/start.html", context)


def nextHeat(request):
    context = {}
    return render(request, "derby/nextHeat.html", context)


def audience(request):
    template = request.GET.get('next', 'derby/leaderboard.html')

    # TODO: this needs to change to be real
    group = Group.objects.get(name="Open")

    if template == 'derby/leaderboard.html':
        context = {"timeout": 10000, "audience": True,
                   "cars": getTimes(group),
                   "next": "derby/nextHeat.html"}
    else:
        context = {}

    return render(request, template, context)


def currentHeat(request):
    context = {}
    return render(request, "derby/currentHeat.html", context)


def remainingHeats(request):
    # needs to be changed to be the color of the group
    context = {"color": "red"}
    return render(request, "derby/remaining.html", context)


def allCars(request):
    context = {"cars": Car.objects.all()}
    return render(request, "derby/allCars.html", context)


def leaderboard(request):
    listCars = [
        {"owner": "DAD", "name": "slowpoke", "picture": "", "speed": "01:07.02"},
        {"owner": "Joshua", "name": "Wabbit",
            "picture": "Wabbit.jpg", "speed": "00:42.42"},
        {"owner": "DAD", "name": "slowpoke", "picture": "", "speed": "01:03.02"},
        {"owner": "Mom", "name": "Filthy Panda Stealer",
            "picture": "", "speed": "00:43.02"},
        {"owner": "Joshua", "name": "Wabbit",
            "picture": "Wabbit.jpg", "speed": "00:49.42"},
        {"owner": "DAD", "name": "slowpoke", "picture": "", "speed": "01:07.02"},
        {"owner": "Mom", "name": "Filthy Panda Stealer",
            "picture": "", "speed": "00:48.02"},
    ]
    context = {"leaderboard": sorted(
        listCars, key=lambda car: car['speed'])[:5]}
    return render(request, "derby/leaderboard.html", context)
