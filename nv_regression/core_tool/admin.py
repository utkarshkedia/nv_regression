from django.contrib import admin
from .models import systems,vbios,processTracker

# Register your models here.
admin.site.register(systems)
admin.site.register(vbios)
admin.site.register(processTracker)
