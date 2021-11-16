from django.shortcuts import render

# Create your views here.
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
    testDetails["cwd"] = request.POST["CWD"]

    p = subprocess.popen("python test.py")