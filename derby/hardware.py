import time
from django.apps import AppConfig
from derby.models import Result, Heat
from threading import Thread
from time import time, sleep, time_ns


class FakeGPIO:
    BOARD = 1
    PUD_UP = 1
    IN = 1

    def __init__(self):
        print("!!!! NO GPIO")

    def setmode(self, *args, **kwargs):
        pass

    def setup(self, *args, **kwargs):
        pass

    def input(self, *args, **kwargs):
        return False


try:
    import RPi.GPIO as GPIO
except:
    GPIO = FakeGPIO()


class Hardware:
    LANE_1 = 33
    LANE_2 = 35
    LANE_3 = 37
    LANE_4 = 36
    LANE_5 = 38
    LANE_6 = 40

    SWITCH_IN = 31

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        self.lanes = [self.LANE_1, self.LANE_2, self.LANE_3,
                      self.LANE_4, self.LANE_5, self.LANE_6]
        GPIO.setup(self.lanes, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.SWITCH_IN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.lane = {}
        self.update()

    def update(self):
        for i in range(1, 7):
            self.lane[i] = True if GPIO.input(self.lanes[i-1]) else False
        self.startSwitchClosed = False if GPIO.input(self.SWITCH_IN) else True


hardware = Hardware()
currentHeat = 0


class RaceTimerThread(Thread):
    def __init__(self, group=None, target=None, name=None):
        self.laneTimes = {}
        self.startTime = 0
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
        # wait for start switch to open
        while hardware.startSwitchClosed:
            hardware.update()
        self.startTime = time_ns()
        sleep(.5)   # give switch time to settle
        while not hardware.startSwitchClosed:
            hardware.update()
            elapsedTimeMs = self.getElapsedTime()
            for i in range(1, 7):
                if hardware.lane[i]:
                    self.setLane(i, elapsedTimeMs)

    # def run(self):
    #     self.runRace()
        # if self.currentHeat:
        #     heat = Heat.objects.get(id=currentHeat)
        #     results = Result.objects.filter(heat=heat)
        #     for result in results:
        #         laneNum = result.lane.number
        #         if result.self.laneTimes[laneNum]:
        #             result.time = time.timedelta(
        #                 milliseconds=result.self.laneTimes[laneNum])
        #             result.save()
        #     heat.finished = True
        #     heat.save()
        # currentHeat = 0
