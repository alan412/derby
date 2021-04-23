import sys
from django.db import models
from django.core.files.uploadedfile import InMemoryUploadedFile
from colorfield.fields import ColorField
from PIL import Image
from io import BytesIO


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
            group=self.group).order_by('-number').first()
        if not lastCar:
            self.number = 1
        else:
            self.number = lastCar.number + 1

    def resizeImage(self, origImage):
        tmpImage = Image.open(origImage).resize((500, 500))
        outputIoStream = BytesIO()
        tmpImage.save(outputIoStream, format='JPEG', quality=60)
        outputIoStream.seek(0)
        return InMemoryUploadedFile(outputIoStream, 'ImageField', "%s.jpg" % tmpImage.name.split('.')[
            0], 'image/jpeg', sys.getsizeof(outputIoStream), None)

    def save(self, *args, **kwargs):
        if not self.id:
            self.picture = self.resizeImage(self.picture)
        super(Car, self).save(*args, **kwargs)

    def __str__(self):
        return f"Car: {self.name} - {self.group} ({self.number})"


class Heat(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    number = models.IntegerField()
    finished = models.BooleanField()

    def assignNumber(self):
        lastHeat = Heat.objects.filter(
            group=self.group).order_by('-number').first()
        if not lastHeat:
            self.number = 1
        else:
            self.number = lastHeat.number + 1

    def __str__(self):
        return f"{self.group.name} ({self.number})"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['group', 'number'], name='Unique heat number in group')
        ]


class Lane(models.Model):
    number = models.IntegerField(unique=True)
    active = models.BooleanField()

    def __str__(self):
        return str(self.number)


class Result(models.Model):
    heat = models.ForeignKey(Heat, on_delete=models.CASCADE)
    lane = models.ForeignKey(Lane, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    time = models.DurationField(null=True)
