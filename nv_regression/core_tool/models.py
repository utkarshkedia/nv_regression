from django.db import models

# Create your models here.
class Sytem(models.Model):
    winHostname = models.CharField(max_length=100, blank=True)
    winUsername = models.CharField(max_length=100, blank=True)
    winPassword = models.CharField(max_length=100, blank=True)
    debHostname = models.CharField(max_length=100, blank=True)
    debUsername = models.CharField(max_length=100, blank=True)
    debPassword = models.CharField(max_length=100, blank=True)
    ubuHostname = models.CharField(max_length=100, blank=True)
    ubuUsername = models.CharField(max_length=100, blank=True)
    ubuPassword = models.CharField(max_length=100, blank=True)
    remark = models.CharField(max_length=200, null=True, blank=True)

class vbios(models.Model):
    chipName = models.CharField(max_length=100)
    memoryType = models.CharField(max_length=100)
    boardName = models.CharField(max_length=100)
    romName = models.CharField(max_length=100)

    def __str__(self):
        return self.name_of_the_gpu

class processTracker(models.Model):
    userEmail = models.CharField(max_length=100)
    procName = models.CharField(max_length=100)