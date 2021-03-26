from django.db import models
from colorfield.fields import ColorField


class Group(models.Model):
    name = models.CharField(max_length=200)
    color = ColorField(unique=True, default='##FF0000')

    def __str__(self):
        return f"Group: {self.name}"


class Car(models.Model):
    name = models.CharField(max_length=200)
    picture = models.ImageField(upload_to="uploads/")
    owner = models.CharField(max_length=200)
    number = models.IntegerField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['group', 'number'], name='Unique car number in group')
        ]

    def assignNumber(self):
        lastCar = Car.objects.filter(
            group=self.group).order_by('number').first()
        if not lastCar:
            self.number = 1
        else:
            self.number = lastCar.number + 1

    def __str__(self):
        return f"Car: {self.name} - {self.group} ({self.number})"


class Heat(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    number = models.IntegerField()
    finished = models.BooleanField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['group', 'number'], name='Unique heat number in group')
        ]


class Result(models.Model):
    heat = models.ForeignKey(Heat, on_delete=models.CASCADE)
    lane = models.IntegerField()
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    time = models.DurationField(null=True)
