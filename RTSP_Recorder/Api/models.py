from django.db import models


class Camera(models.Model):
    name = models.CharField(max_length=50,default="undefined")
    url = models.CharField(max_length=150)
    status = models.BooleanField(default=False)
    active_hours = models.CharField(max_length=50,default="9AM TO 9PM")

class Recording(models.Model):
    name = models.CharField(max_length=100)
    path = models.CharField(max_length=150)
    status = models.CharField(max_length=50)
    datetime = models.CharField(max_length=50)

