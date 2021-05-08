from derby.models import Heat, Car, Lane, Result
from random import randrange


def getAvailableCars(cars, lane, newHeat):
    notEligible = Result.objects.filter(car__in=cars) & \
        (Result.objects.filter(heat=newHeat) |
         Result.objects.filter(lane=lane))
    notEligibleCars = set(result.car for result in notEligible)

    return list(set(cars) - set(notEligibleCars))


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
