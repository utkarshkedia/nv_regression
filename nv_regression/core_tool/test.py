import json,sys,os
from.views import killTest
from .models import processTracker,vbios,systems
from threading import Thread
import paramiko
from scp import SCPClient
import time

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

    startTest(jsonCfg,settings)

def startTest(jsonCfg,settings):

    #setting Default Parameters
    baseDir = Path(__file__).resolve().parent.parent
    if jsonCfg["cwd"] == '':
        jsonCfg["cwd"] = settings["defaultCWD"]

    #create ROM list
    romPathList = []
    romVersionList = []
    if jsonCfg["vbiosFlash"] == '':
        pass
    else:
        if jsonCfg["vbiosFlash"]["shmooStatus"] == False:
            if jsonCfg["vbiosFlash"]["vbiosDirectory"] != '':
                romPath = jsonCfg["vbiosFlash"]["vbiosDirectory"]
                romName = romPath.split("\\").split[-1]
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

    if romPathList.len() == 0:
        romPathList.append("nullElement")

    for romPath in romPathList:
        shmooIndex = romPathList.index(romPath)
        if romPath == "nullElement" :
            pass
        else:
            #transfer the ROM
            try:
                with SCPClient(ssh.get_transport()) as scp:
                    scp.put(romPath, jsonCfg["cwd"])
            except:
                ###

            #transfer nvmt
            try:
                with SCPClient(ssh.get_transport()) as scp:
                    scp.put(settings["nvmt"], jsonCfg["cwd"])
            except:
                ###

            #transfer nvflash shell file
            try:
                with SCPClient(ssh.get_transport()) as scp:
                    scp.put(os.path.join(baseDir,settings["testSystemFilesBaseDir"],"nvflash.sh"), jsonCfg["cwd"])
            except:
                ####

            #Edit and start flashing
            fileObject = sftp.file(os.path.join(jsonCfg["cwd"],"nvflash.sh"), 'r+')
            testCommands = fileObject.readlines()
            fileObject.close()
            n = len(test_commands)
            testCommands[0] = "cd " + jsonCfg["cwd"] + "\n"
            testCommands[2] = "./nvflash_eng -A" + " " + romName
            for param in jsonCfg["vbiosFlash"]["params"]:
                testCommands[2] = testCommands[2] + " " + param
            testCommands[2] = testCommands[2] + " >> nvflash.log\n"
            fileObject = sftp.file(os.path.join(jsonCfg["cwd"],"nvflash.sh"), 'w+')
            fileObject.writelines(testCommands)
            fileObject.close()

            # running the test
            testRunCommand = os.path.join(jsonCfg["cwd"],"nvflash.sh")
            ssh.exec_command(testRunCommand)

            time.sleep(30)

        for modsPath in modsPathList:
            modsShmooIndex = modsPathList.index(modsPath)
            modsVersion = modsVersionList[modsShmooIndex]
            if jsonCfg["modsTest"]["modsPresent"] == True:
                pass
            else:
                #transfer MODS to the CWD
                if shmooIndex == 0:
                    try:
                        sftp.mkdir(os.path.join(jsonCfg["cwd"],modsVersion))
                        files = os.listdir(modsPath)
                        for file in files:
                            path = os.path.join(modsPath,file)
                            with SCPClient(ssh.get_transport()) as scp:
                                scp.put(path, os.path.join(jsonCfg["cwd"],modsVersion))
                    except:
                        with open(result_path + hostname + 'Exceptions.txt', 'a+') as f:
                            f.write("Cannot copy Mods to the romote system\n")

                    # transfer extract.py to the test system
                    try:
                        with SCPClient(ssh.get_transport()) as scp:
                            scp.put(os.path.join(baseDir,settings["testSystemFilesBaseDir"],"extract.py"),settings["testSystemBaseDir"])
                    except:

                    fileObject = sftp.file(os.path.join(settings["testSystemBaseDir"],"extract.py"), 'r+')
                    contents = fileObject.readlines()
                    contents[2] = "files=os.listdir(" + "'" + cwd + "'" + ")" + "\n"
                    contents[5] = "    path=" + "'" + cwd + "'" + "+ '/' + file" + "\n"
                    fileObject.close()
                    fileObject = sftp.file(os.path.join(settings["testSystemBaseDir"],"extract.py"), 'w+')
                    fileObject.writelines(contents)
                    fileObject.close()

                    ssh.exec_command('python3 /localhome/lab/extract.py')

                #Run MODS Test











