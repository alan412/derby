from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from derby.forms import RegisterForm
from derby.models import Car, Group, Heat, Result
from derby.generateHeats import generateHeats
from derby.getTimes import getTimes
from derby.hardware import hardware, RaceTimerThread
from time import sleep

currentHeat = None


def groupFromId(groupId):
    return Group.objects.get(id=groupId)


hwThread = None


def getNextHeat(group):
    return Heat.objects.filter(
        group=group, finished=False).order_by('number').first()


def heatData(request):
    global hwThread
    global currentHeat

    data = {'finished': not hwThread.is_alive()}
    if hwThread.startTime:
        data['time'] = hwThread.getElapsedTime()
    else:
        data['time'] = 0

    for lane in range(1, 7):
        if lane in hwThread.laneTimes:
            data[str(lane)] = hwThread.laneTimes[lane]

    if data['finished']:
        if currentHeat:
            hwThread.saveHeat(currentHeat)
            currentHeat = getNextHeat(currentHeat.group)
            if currentHeat:
                hwThread.start()

    return JsonResponse(data)


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
    context = {'groups': Group.objects.all()}
    return render(request, "derby/main.html", context)


def testHardware(request):
    context = {'interval': 200}
    return render(request, "derby/testHardware.html", context)


def updateHardware(request):
    hardware.update()
    lanes = []
    for i in range(1, 7):
        lanes.append({'number': i, "status": hardware.lane[i]})

    context = {'lanes': lanes,
               "startSwitchClosed": hardware.startSwitchClosed}
    return render(request, "derby/hwTable.html", context)


def start(request, groupId):
    global currentHeat
    global hwThread
    group = groupFromId(groupId)
    generateHeats(group)
    # sets global
    try:
        currentHeat = getNextHeat(group)
        if not hwThread:
            hwThread = RaceTimerThread()
        else:
            if not hwThread.done:
                hwThread.done = True
                while hwThread.isAlive():
                    sleep(.1)

        hwThread.start()
    except Heat.DoesNotExist:
        currentHeat = None

    return audience(request, groupId)


def audience(request, groupId):
    global currentHeat
    template = request.GET.get('next', 'derby/currentHeat.html')

    if template == 'derby/leaderboard.html':
        context = {"timeout": 10_000, "audience": True,
                   "next": "derby/currentHeat.html"}
        return showLeaderboard(request, context, groupId)
    elif template == 'derby/currentHeat.html':
        group = groupFromId(groupId)
        context = {"timeout": 5_000, "audience": True,
                   "heat": currentHeat,
                   "totalHeats": Heat.objects.filter(group=group).count(),
                   "interval": 250,
                   "next": "derby/leaderboard.html"}
        if currentHeat:
            results = Result.objects.filter(heat=currentHeat)
            context["results"] = results
        else:
            return redirect('/')
    else:
        context = {}

    return render(request, template, context)


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
