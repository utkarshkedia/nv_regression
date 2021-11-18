from django.shortcuts import render
from .models import processTracker, vbios, systems
import subprocess, os
from rest_framework.response import Response
from django.http import HttpResponse
import datetime
from .serializers import vbiosSerializer, processTrackerSerializer, systemsSerializer
import psutil
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

# Create your views here.
class processTracker(APIView):

    def get(self,request):
        processDetails = processTracker.objects.all()
        serializer = processTrackerSerializer(processDetails, many=True)
        return Response(serializer.data)

class vbiosInfo(APIView):

    def get(self,request):
        vbiosDetails = vbios.objects.all()
        serializer = vbiosSerializer(vbiosDetails, many=True)
        return Response(serializer.data)
    def post(self,request):
        serializer = vbiosSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class systemsDetail(APIView):

    def get(self,request):
        systemDetails = systems.objects.all()
        serializer = systemsSerializer(systemDetails, many=True)
        return Response(serializer.data)


def startTest(request):
    testDetails = {}

    #userDetail
    testDetails["userID"]

    #systemDetail
    testDetails["systemIDs"] = request.POST['System_IDs']

    #vbiosDetail
    if 'is_VBIOS_Regression' in request.POST:
        testDetails["vbiosFlash"]["vbiosDirectory"] = request.POST["VBIOS_Directory"].strip()
        testDetails["vbiosFlash"]["vbiosID"] = request.POST["VBIOS_ID"].strip()
        testDetails["vbiosFlash"]["params"] = []
        if 'param0' in request.POST:
            testDetails["vbiosFlash"]["params"].append('-4')
        if 'param1' in request.POST:
            testDetails["vbiosFlash"]["params"].append('-5')
        if 'param2' in request.POST:
            testDetails["vbiosFlash"]["params"].append('-6')
        if 'is_VBIOS_Shmoo' in request.POST:
            testDetails["vbiosFlash"]["shmooStatus"] = True
            testDetails["vbiosFlash"]["shmooType"] = "normal"
            testDetails["vbiosFlash"]["shmooInitial"] = request.POST["VBIOS_Shmoo_Initial"].strip()
            testDetails["vbiosFlash"]["shmooFinal"] = request.POST["VBIOS_Shmoo_Final"].strip()
        elif 'is_CL_Based_Shmoo' in request.POST:
            testDetails["vbiosFlash"]["shmooStatus"] = True
            testDetails["vbiosFlash"]["shmooType"] = "clBased"
            testDetails["vbiosFlash"]["shmooInitial"] = request.POST["VBIOS_Shmoo_Initial"].strip()
            testDetails["vbiosFlash"]["shmooFinal"] = request.POST["VBIOS_Shmoo_Final"].strip()
        else:
            testDetails["vbiosFlash"]["shmooStatus"] = False
    else:
        testDetails["vbiosFlash"] = ''

    #modsDetails
    if 'is_MODS_Test' in request.POST:
        testDetails["modsTest"]["modsFamily"]=request.POST["MODS_Family"].strip()

        if 'Test0' in request.POST:
            testDetails["modsTest"]["Test"] = "modsInit"
        elif 'Other_Test' in request.POST:
            testDetails["modsTest"]["Test"] = request.POST["MODS_Test_Number"].strip()

        testDetails["modsTest"]["Arguments"] = request.POST["MODS_Test_Arguments"].strip()
        if 'is_MODS_Shmoo' in request.POST:
            testDetails["modsTest"]["shmooStatus"] = True
            testDetails["modsTest"]["shmooInitial"] = request.POST["MODS_Shmoo_Initial"].strip()
            testDetails["modsTest"]["shmooFinal"] = request.POST["MODS_Shmoo_Final"].strip()
        else:
            testDetails["modsTest"]["shmooStatus"] = False
    else:
        testDetails["modsTest"] = ''


    #driverDetails
    if 'is_Driver_Test' in request.POST:
        testDetails["driverTest"]["driverFamily"]=request.POST["DRIVER_Family"].strip()
        if 'is_DRIVER_Shmoo' in request.POST:
            testDetails["driverTest"]["shmooStatus"] = True
            testDetails["driverTest"]["shmooInitial"] = request.POST["DRIVER_Shmoo_Initial"].strip()
            testDetails["driverTest"]["shmooFinal"] = request.POST["DRIVER_Shmoo_Final"].strip()
        else:
            testDetails["driverTest"]["shmooStatus"] = False
    else:
        testDetails["driverTest"] = ''

    #autocharDetails
    if 'is_Autochar' in request.POST:
        testDetails["autocharTest"]["apps"] = []
        for i in range(1, 22):
            if 'app' + str(i) in request.POST:
                testDetails["autocharTest"]["apps"].append(request.POST['app' + str(i)])

        if 'is_Autochar_Configure' in request.POST:
            testDetails["configureAutochar"] = True
            testDetails["configureAutochar"]["regWrite"] = []
            for i in range(1, 11):
                if request.POST['iteration' + str(i)] != '':
                    testDetails["configureAutochar"]["regWrite"].append(request.POST['iteration' + str(i)])
            testDetails["configureAutochar"]["nvvdd"] = request.POST["NVVDD"].strip()
            testDetails["configureAutochar"]["gpcclkInitial"] = request.POST["GPCCLK_Initial"].strip()
            testDetails["configureAutochar"]["gpcclkFinal"] = request.POST["GPCCLK_Final"].strip()
            testDetails["configureAutochar"]["mclkInitial"] = request.POST["MCLK_Initial"].strip()
            testDetails["configureAutochar"]["mclkFinal"] = request.POST["MCLK_Final"].strip()
            testDetails["configureAutochar"]["mclkStep"] = request.POST["MCLK_Step"].strip()
            testDetails["configureAutochar"]["gpcclkStep"] = request.POST["GPCCLK_Step"].strip()
        else:
            testDetails["configureAutochar"] = False
    else:
        testDetails["autocharTest"] = ''


    #cwd
    testDetails["cwd"] = request.POST["CWD"].strip()

    p = subprocess.popen("python test.py")
    pid = p.pid

    saveProc(pid)

    return redirect('/links')


def saveProc(request,procId):
    processObject = processTracker(userEmail=request.user.email, procName=request.POST['pName'], procId=int(procId), timeCreated=datetime.datetime.now())
    processObject.save()
    os.waitpid(int(procId))
    killTest(int(procId))

def killTest(request,procId):

    if request.user.is_authenticated:
        try:
            proc = processTracker.objects.get(procId=int(procId))
            if proc.userEmail.strip() == request.user.email.strip():
                proc.delete()
                if psutil.pid_exists(int(procId)):
                    os.kill(int(procId))
        except:
            return HttpResponse("This process does not exist")

        else:
            return HttpResponse("You are not authorised to kill this process")
    else:
        return HttpResponse("Login First")


def testInit(request):
    return render(request,'testInit.html')

def home(request):
    return render(request,'home.html')

def killInit(request):
    return render(request,'killTest.html')

