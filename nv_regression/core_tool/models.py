from django.db import models

# Create your models here.
class systems(models.Model):
    winHostname = models.CharField(max_length=100, blank=True)
    winUsername = models.CharField(max_length=100, blank=True)
    winPassword = models.CharField(max_length=100, blank=True)
    winBootIndex = models.IntegerField()
    debHostname = models.CharField(max_length=100, blank=True)
    debUsername = models.CharField(max_length=100, blank=True)
    debPassword = models.CharField(max_length=100, blank=True)
    debBootIndex = models.IntegerField()
    ubuHostname = models.CharField(max_length=100, blank=True)
    ubuUsername = models.CharField(max_length=100, blank=True)
    ubuPassword = models.CharField(max_length=100, blank=True)
    ubuBootIndex = models.IntegerField()
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
    procName = models.CharField(max_length=100,blank=True)
    procId = models.IntegerField(primary_key=True)
    timeCreated = models.DateTimeField()