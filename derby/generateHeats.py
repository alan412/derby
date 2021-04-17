from derby.models import Heat, Car, Lane, Result


class CarForSorting:
    def __init__(self, car):
        self.car = car
        self.lastPosition = 0

        lastResult = Result.objects.filter(
            car=car).order_by('-heat__number')
        if lastResult:
            self.lastPosition = (lastResult[0].heat.number *
                                 100) + (100 - lastResult[0].lane.number)

    def __repr__(self):
        return f"{self.car.name} - {self.lastPosition}"


def hasCarBeenInLane(car, lane):
    try:
        Result.objects.get(car=car, lane=lane)
    except Result.DoesNotExist:
        return False
    return True


def generateHeats(group):
    done = False

    while not done:
        newHeat = Heat()
        newHeat.group = group
        newHeat.finished = False
        newHeat.assignNumber()

        # add ordered by last heat it was in.
        carsInGroup = Car.objects.filter(group=group)
        if not carsInGroup:
            return
        sortedCars = sorted([CarForSorting(car)
                             for car in carsInGroup], key=lambda car: car.lastPosition)
        print(sortedCars)
        carPlaced = []
        for lane in Lane.objects.filter(active=True):
            for sortedCar in sortedCars:
                car = sortedCar.car
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
