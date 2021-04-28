from derby.models import Heat, Car, Lane, Result
from random import randrange


def hasCarBeenInLane(car, lane):
    try:
        Result.objects.get(car=car, lane=lane)
    except Result.DoesNotExist:
        return False
    return True


def hasCarBeenInHeat(car, heat):
    try:
        Result.objects.get(car=car, heat=heat)
    except Result.DoesNotExist:
        return False
    return True


def getAvailableCars(cars, lane, newHeat):
    listCars = []
    # get list of cars not in this heat and not already in this lane
    for car in cars:
        if hasCarBeenInLane(car, lane):
            continue
        if hasCarBeenInHeat(car, newHeat):
            continue
        listCars.append(car)
    return listCars


def generateHeats(group):
    done = False

    carsInGroup = Car.objects.filter(group=group)
    listLanes = list(Lane.objects.filter(active=True))
    if not carsInGroup:
        return

    while not done:
        newHeat = Heat()
        newHeat.group = group
        newHeat.finished = False
        newHeat.assignNumber()

        carPlaced = []
        for lane in listLanes:
            listCars = getAvailableCars(carsInGroup, lane, newHeat)
            print(lane, listCars)
            if listCars and len(listCars):
                # Randomly pick car
                car = listCars[randrange(0, len(listCars))]
                newHeat.save()
                newResult = Result(heat=newHeat, lane=lane, car=car)
                newResult.save()
                carPlaced.append(car)
        listLanes.reverse()
        if not carPlaced:
            done = True
