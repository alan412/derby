from django.apps import AppConfig
from derby.models import Result, Heat
from threading import Thread
from time import sleep, time_ns
from datetime import timedelta


class FakeGPIO:
    BOARD = 1
    PUD_UP = 1
    IN = 1

    def __init__(self):
        print("!!!! NO GPIO")
        self.pins = {}

    def setPin(self, pin, value):
        self.pins[pin] = value

    def setmode(self, *args, **kwargs):
        pass

    def setup(self, *args, **kwargs):
        pass

    def input(self, pin):
        sleep(0.01)
        if pin not in self.pins:
            return False
        return self.pins[pin]


fakeHardware = False
try:
    import RPi.GPIO as GPIO
except:
    GPIO = FakeGPIO()
    fakeHardware = True


class Hardware:
    LANE_6 = 33
    LANE_5 = 35
    LANE_4 = 37
    LANE_3 = 36
    LANE_2 = 38
    LANE_1 = 40

    SWITCH_IN = 31

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        self.lanes = [self.LANE_1, self.LANE_2, self.LANE_3,
                      self.LANE_4, self.LANE_5, self.LANE_6]
        GPIO.setup(self.lanes, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.SWITCH_IN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.lane = {}
        self.update()

    def setValue(self, pin, value):
        if fakeHardware:
            GPIO.setPin(pin, True if value else False)
        else:
            print("CAN'T FAKE REAL HARDWARE!!!")

    def update(self):
        for i in range(1, 7):
            self.lane[i] = True if GPIO.input(self.lanes[i-1]) else False

        self.startSwitchClosed = False if GPIO.input(self.SWITCH_IN) else True


hardware = Hardware()


class RaceTimerThread(Thread):
    def __init__(self, group=None, target=None, name=None):
        self.laneTimes = {}
        self.startTime = 0
        self.done = True
        super(RaceTimerThread, self).__init__(
            group=group, target=target, name=name)

    def getElapsedTime(self):
        return (time_ns() - self.startTime) / 1_000_000

    def setLane(self, laneNum, elapsedTime):
        if laneNum not in self.laneTimes:
            self.laneTimes[laneNum] = elapsedTime

    def run(self):
        self.laneTimes = {}
        self.startTime = 0
        self.done = False
        sleep(.5)  # give switch time to settle
        # wait for start switch to open
        while not self.done:
            hardware.update()
            if not hardware.startSwitchClosed:
                break

        self.startTime = time_ns()
        if not self.done:
            sleep(.5)   # give switch time to settle
        while not self.done:
            hardware.update()
            elapsedTimeMs = self.getElapsedTime()
            for i in range(1, 7):
                if hardware.lane[i]:
                    self.setLane(i, elapsedTimeMs)
            if hardware.startSwitchClosed:
                self.done = True

    def saveHeat(self, heat):
        if heat:
            results = Result.objects.filter(heat=heat)
            for result in results:
                laneNum = result.lane.number
                if laneNum in self.laneTimes:
                    result.time = timedelta(
                        milliseconds=self.laneTimes[laneNum])
                    result.save()
            heat.finished = True
            heat.save()
        self.laneTimes = {}
        self.startTime = 0
        self.done = True
