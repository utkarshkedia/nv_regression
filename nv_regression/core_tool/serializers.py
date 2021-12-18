from rest_framework import serializers
from .models import vbios,processTracker,systems

class vbiosSerializer(serializers.ModelSerializer):
    class Meta:
        model = vbios
        fields = ('id','chipName','memoryType','boardName','romName')

class systemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = systems
        fields = ('id','winHostname','winBootIndex','debHostname','debBootIndex','ubuHostname','ubuBootIndex','currentOS','remark')

class processTrackerSerializer(serializers.ModelSerializer):
    class Meta:
        model = processTracker
        fields = ('id','procName','username','timeCreated')
