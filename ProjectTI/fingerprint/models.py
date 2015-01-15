from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Fingerprint(models.Model):
    user = models.ForeignKey(User, unique=True)
    template = models.CharField(max_length=5000)

    def __str__(self):
        return self.user.username

class Door(models.Model):
    name = models.CharField(max_length=200)
    allowed_users = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.name

class Log(models.Model):
    user = models.ForeignKey(User)
    door = models.ForeignKey(Door)
    datetime = models.DateTimeField('record time')
    message = models.TextField(max_length=800)

    def __str__(self):
        return self.door.name

class Privilege(models.Model):
    user = models.ForeignKey(User, unique=True)
    privilege = models.CharField(max_length=100)
