from django.http.response import HttpResponse, JsonResponse
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
    nextHeat = Heat.objects.filter(
        group=group, finished=False).order_by('number').first()
    print("---Next Heat", nextHeat)
    return nextHeat


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
        hwThread = None

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
    if hwThread:
        hwThread.done = True
        while hwThread.isAlive():
            sleep(.1)
        hwThread = None
    group = groupFromId(groupId)
    generateHeats(group)
    # sets global
    try:
        currentHeat = getNextHeat(group)
        hwThread = RaceTimerThread()
        hwThread.start()
    except Heat.DoesNotExist:
        currentHeat = None
    return audience(request, groupId)


def fake(request):
    global hardware
    hardware.setValue(hardware.SWITCH_IN, request.GET.get('sw', 0))
    hardware.setValue(hardware.LANE_1, request.GET.get('1', 0))
    hardware.setValue(hardware.LANE_2, request.GET.get('2', 0))
    hardware.setValue(hardware.LANE_3, request.GET.get('3', 0))
    hardware.setValue(hardware.LANE_4, request.GET.get('4', 0))
    hardware.setValue(hardware.LANE_5, request.GET.get('5', 0))
    hardware.setValue(hardware.LANE_6, request.GET.get('6', 0))
    return HttpResponse("Fake Hardware set")


def audience(request, groupId):
    global currentHeat
    global hwThread
    template = request.GET.get('next', 'derby/currentHeat.html')

    if template == 'derby/leaderboard.html':
        context = {"timeout": 15_000, "audience": True,
                   "next": "derby/currentHeat.html"}
        return showLeaderboard(request, context, groupId)
    elif template == 'derby/currentHeat.html':
        group = groupFromId(groupId)
        context = {"timeout": 15_000, "audience": True,
                   "heat": currentHeat,
                   "totalHeats": Heat.objects.filter(group=group).count(),
                   "interval": 200,
                   "next": "derby/leaderboard.html"}
        if currentHeat:
            results = Result.objects.filter(
                heat=currentHeat).order_by("lane")
            context["results"] = results
            if not hwThread:
                hwThread = RaceTimerThread()
                hwThread.start()
        else:
            return redirect('/')
    else:
        context = {}

    return render(request, template, context)


def allHeats(request, groupId):
    group = groupFromId(groupId)
    heatObjects = Heat.objects.filter(group=group)
    heats = []
    for heat in heatObjects:
        heats.append({"number": heat.number,
                      "results": Result.objects.filter(heat=heat).order_by("lane")})

    context = {
        "group": group,
        "heats": heats,
        "totalHeats": len(heats)
    }
    print(context)

    return render(request, "derby/allHeats.html", context)


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
