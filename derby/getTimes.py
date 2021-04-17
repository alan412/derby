from derby.models import Heat, Car, Lane, Result
import datetime


class CarWithTime:
    def __init__(self, car, fastestTime):
        self.car = car
        self.fastestTime = fastestTime


def getTimes(group):
    listCars = []
    carsInGroup = Car.objects.filter(group=group)
    if not carsInGroup:
        return
    for car in carsInGroup:
        results = Result.objects.filter(
            car=car).exclude(time__isnull=True).order_by("time")
        if results:
            result = results[0]
            listCars.append(CarWithTime(car, result.time))
        else:
            listCars.append(CarWithTime(car, datetime.timedelta()))

    # This should give us cars sorted by fastest time
    return sorted(listCars, key=lambda car: car.fastestTime if car.fastestTime else datetime.timedelta(days=1))
