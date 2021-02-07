from django.db import models


class Group(models.Model):
    name = models.CharField(max_length=200)


class Car(models.Model):
    name = models.CharField(max_length=200)
    picture = models.ImageField()
    owner = models.CharField(max_length=200)
    number = models.IntegerField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['group', 'number'], name='Unique car number in group')
        ]


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
