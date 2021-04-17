from derby.models import Heat, Car, Lane, Result


def hasCarBeenInLane(car, lane):
    try:
        Result.objects.get(car=car, lane=lane)
    except Result.DoesNotExist:
        return False
    return True


def generateHeats(group):
    done = False

    carsInGroup = Car.objects.filter(group=group)
    if not carsInGroup:
        return
    carList = list(carsInGroup)
    while not done:
        newHeat = Heat()
        newHeat.group = group
        newHeat.finished = False
        newHeat.assignNumber()

        carPlaced = []
        for lane in Lane.objects.filter(active=True):
            for car in carList:
                if car in carPlaced:
                    continue
                # car hasn't been in lane
                if not hasCarBeenInLane(car, lane):
                    newHeat.save()
                    newResult = Result()
                    newResult.heat = newHeat
                    newResult.lane = lane
                    newResult.car = car
                    newResult.save()
                    carPlaced.append(car)
                    break
        if not carPlaced:
            done = True
        else:
            carList = carList[1:] + [carList[0]]
