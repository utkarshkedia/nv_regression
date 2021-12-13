import json,sys,os
from.views import killTest
from .models import processTracker,vbios,systems
from threading import Thread

procId = os.getpid()
if __name__ == "__main__":
    username = sys.argv[1]

    baseDir = Path(__file__).resolve().parent.parent

    configParentPenDir = os.path.join(baseDir, "config_files")
    configParentDir = os.path.join(configParentPenDir,username)
    try:
        with open(os.path.join(configParentDir,"config.json"),'r') as json_file:
            jsonCfg = json.load(json_file)
    except Exception as e:

    settingsParentDir = os.path.join(baseDir, "settings")
    try:
        with open(os.path.join(settingsParentDir,"settings.json"),'r') as json_file:
            settings = json.load(json_file)
    except Exception as e:

    systemIDs = jsonCfg["systemIDs"]
    systemIDs = systemIDs.split(",")
    n = len(systemIDs)
    for i in range(n):
        Thread

def startTest(jsonCfg,settings,systemID):

    #create ROM list
    romPathList = []
    romVersionList = []
    if jsonCfg["vbiosFlash"] == '':
        pass
    else:
        if jsonCfg["vbiosFlash"]["shmooStatus"] == False:
            if jsonCfg["vbiosFlash"]["vbiosDirectory"] != '':
                romPath = jsonCfg["vbiosFlash"]["vbiosDirectory"]
            else:
                vbiosID = jsonCfg["vbiosFlash"]["vbiosID"]
                chipName = vbios.objects.get(id=int(vbiosID)).chipName
                memoryType = vbios.objects.get(id=int(vbiosID)).memoryType
                boardName = vbios.objects.get(id=int(vbiosID)).boardName
                romName = vbios.objects.get(id=int(vbiosID)).romName
                try:
                    dirPath = settings["vbiosBaseDir"][0]+ '\\' + chipName
                    allFiles = os.listdir(dirPath)
                    ctime = 0
                    for file in allFiles:
                        if file.endswith("DO_NOT_USE"):
                            pass
                        else:
                            parentPath = dirPath + '\\' + file
                            if os.path.getctime(parentPath) > ctime:
                                ctime = os.path.getctime(parentPath)
                                latest_path = parentPath
                                latest_file = file
                                romPath = latest_path + '\\' + settings["vbiosBaseDir"][1] + '\\' + memoryType + '\\' + boardName + '\\' + settings["vbiosBaseDir"][2] + '\\' + romName
                except Exception as e:
                    ######
                romPathList.append(romPath)
                romVersionList.append(latest_file)
        else:
            vbiosID = jsonCfg["vbiosFlash"]["vbiosID"]
            chipName = vbios.objects.get(id=int(vbiosID)).chipName
            memoryType = vbios.objects.get(id=int(vbiosID)).memoryType
            boardName = vbios.objects.get(id=int(vbiosID)).boardName
            romName = vbios.objects.get(id=int(vbiosID)).romName
            initialROMVersion = jsonCfg["vbiosFlash"]["shmooInitial"]
            finalROMVersion = jsonCfg["vbiosFlash"]["shmooFinal"]
            if jsonCfg["vbiosFlash"]["shmooType"] == "normal":
                try:
                    initialROMVersionDir = settings["vbiosBaseDir"][0] + '\\' + chipName + '\\' + initialROMVersion
                    initialTime = os.path.getctime(initialROMVersionDir)
                    finalROMVersionDir = settings["vbiosBaseDir"][0] + '\\' + chipName + '\\' + finalROMVersion
                    endTime = os.path.getctime(finalROMVersionDir)
                    dirPath = line1 + '\\' + gpu_name
                    allFiles = os.listdir(dirPath)
                    for file in allFiles:
                        if file.endswith("DO_NOT_USE"):
                            pass
                        else:
                            parentPath = dirPath + '\\' + file
                            if os.path.getctime(parentPath) >= initialTime and os.path.getctime(parentPath) <= endTime:
                                romPath = parentPath + '\\' + settings["vbiosBaseDir"][1] + '\\' + memoryType + '\\' + boardName + '\\' + settings["vbiosBaseDir"][2] + '\\' + romName
                                romPathList.append(romPath)
                                romVersionList.append(file)
                except:
                    ######
            else:
                try:
                    initialROMVersionDir = settings["vbiosClBaseDir"][0] + '\\' + chipName + '\\' + initialROMVersion
                    initialTime = os.path.getctime(initialROMVersionDir)
                    finalROMVersionDir = settings["vbiosClBaseDir"][0] + '\\' + chipName + '\\' + finalROMVersion
                    endTime = os.path.getctime(finalROMVersionDir)
                    dirPath = line1 + '\\' + gpu_name
                    allFiles = os.listdir(dirPath)
                    for file in allFiles:
                        if file.endswith("DO_NOT_USE"):
                            pass
                        else:
                            parentPath = dirPath + '\\' + file
                            if os.path.getctime(parentPath) >= initialTime and os.path.getctime(parentPath) <= endTime:
                                romPath = parentPath + '\\' + settings["vbiosClBaseDir"][1] + '\\' + memoryType + '\\' + boardName + '\\' + settings["vbiosClBaseDir"][2] + '\\' + romName
                                romPathList.append(romPath)
                                romVersionList.append(file)
                except:
                    ######

    #create MODS list
    modsPathList = []
    modsVersionList = []
    if jsonCfg["modsTest"] == '':
        pass
    else:
        modsFamily = jsonCfg["modsTest"]["modsFamily"]
        modsFamilyPath = os.path.join(settings["ModsFamilyPenPath"], modsFamily)
        if jsonCfg["modsTest"]["shmooStatus"] == False:
            try:
                allFiles = os.listdir(ModsFamilyPath)
                ctime = 0
                for file in allFiles:
                    if file.endswith("DO_NOT_USE"):
                        pass
                    else:
                        path = os.path.join(modsFamilyPath,file)
                        if os.path.getctime(path) > ctime:
                            ctime = os.path.getctime(path)
                            modsPath = path
                            modsFile = file
            except Exception as e:
                ############
            modsPathList.append(modsPath)
            modsVersionList.append(modsFile)
        else:
            initialModsVersion = jsonCfg["modsTest"]["shmooInitial"]
            finalModsVersion = jsonCfg["modsTest"]["shmooFinal"]
            initialModsVersionDir = os.path.join(modsFamilyPath,initialModsVersion)
            initialTime = os.path.getctime(initialModsVersionDir)
            finalModsVersionDir = os.path.join(modsFamilyPath,finalModsVersion)
            endTime = os.path.getctime(finalModsVersionDir)
            try:
                allFiles = os.listdir(modsFamilyPath)
                for file in allFiles:
                    if file.endswith("DO_NOT_USE"):
                        pass
                    else:
                        path = os.path.join(modsFamilyPath,file)
                        if os.path.getctime(path) >= initialTime and os.path.getctime(path) <= endTime:
                            modsPathList.append(path)
                            modsVersionList.append(file)
            except:
                ######



    # connect to the test system









