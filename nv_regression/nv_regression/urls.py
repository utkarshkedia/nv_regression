"""nv_regression URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from core_tool import views as v1
from userAuthentication import views as v2


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',v1.home),
    path('register/',v2.register),
    path('killInit/',v1.killInit),
    path('killInit/killTest',v1.killTest),
    path('ongoingTests/',v1.processViewer.as_view()),
    path('vbiosDatabase/',v1.vbiosInfo.as_view()),
    path('systemDatabase/',v1.systemsDetail.as_view()),
    path('testInit/',v1.testInit),
    path('testInit/runTest',v1.startTest),
    path("",include("django.contrib.auth.urls")),
]
