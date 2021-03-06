from django.test import TestCase
import json,sys,os
from models import processTracker,vbios,systems
from threading import Thread
import paramiko
from scp import SCPClient
import time
from datetime import datetime
import smtplib
from email.message import EmailMessage

def send_mail(recepientsEmail):
    baseDir = Path(__file__).resolve().parent.parent

    settingsParentDir = os.path.join(baseDir, "settings")
    with open(os.path.join(settingsParentDir, "settings.json"), 'r') as json_file:
        settings = json.load(json_file)

    configParentPenDir = os.path.join(baseDir, "config_files")
    configParentDir = os.path.join(configParentPenDir, username, str(userProcNum))
    with open(os.path.join(configParentDir, "finalResults.txt"), 'r+') as results:
        finalResult = results.readlines()

    msg = EmailMessage()
    msg['Subject'] = 'nv_regression tool update'
    msg['From'] = settings["outlookEmail"]
    msg['To'] = recepientsEmail
    content = ""
    for result in finalResult:
        content = content + result
    msg.set_content(content)

    with smtplib.SMTP('outlook.office365.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        emailPwd = settings["outlookPassword"]
        email = settings["outlookEmail"]
        smtp.login(email, emailPwd)
        smtp.send_message(msg)

def changeFlag(jsonCfg, username, userProcNum, flag, userEmail):
    systemIDs = jsonCfg["systemIDs"]
    systemID = jsonCfg["systemID"]
    index = systemIDs.index(systemID)
    proc = processTracker.objects.get(userProcNum = userProcNum,username=username)
    if flag == 1:
        flags = proc.modsRunningStatus.split(",")
        if flags[index] == 'f':
            flags[index] = 't'
        else:
            flags[index] = 'f'
        newFlags = ""
        for flag in flags:
            newFlags = newFlags + flag + ","
        proc.modsRunningStatus = newFlags
        proc.save()
    elif flag == 2:
        flags = proc.testCompletionStatus.split(",")
        if flags[index] == 'f':
            flags[index] = 't'
        else:
            flags[index] = 'f'
        newFlags = ""
        for flag in flags:
            newFlags = newFlags + flag + ","
        proc.testCompletionStatus = newFlags
        proc.save()

        # delete proc object from the procTracker database
        testCompleted = True
        for flag in newFlags:
            if flag == "f":
                testCompleted = False
        if testCompleted == True:
            proc.delete()
            send_mail(userEmail)

        #safe fail mechanism in case this process does not terminate itself
        os.kill(procId)

def startTest(jsonCfg,settings,username,userProcNum,userEmail,configParentDir):

    #setting Default Parameters
    baseDir = Path(__file__).resolve().parent.parent
    if jsonCfg["cwd"] == '':
        jsonCfg["cwd"] = settings["defaultCWD"]
    date = datetime.now().strftime("%d%m%Y_%H%M%S")

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
                try:
                    vbiosID = jsonCfg["vbiosFlash"]["vbiosID"]
                    chipName = vbios.objects.get(id=int(vbiosID)).chipName
                    memoryType = vbios.objects.get(id=int(vbiosID)).memoryType
                    boardName = vbios.objects.get(id=int(vbiosID)).boardName
                    romName = vbios.objects.get(id=int(vbiosID)).romName
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
                    finalMessage.append("For {}, Failed to access ROM file".format(debHostname) + "\n")
                    with open(os.path.join(configParentDir, "finalResults.txt"), 'w+') as results:
                        results.writelines(finalMessage)
                    changeFlag(jsonCfg, username, userProcNum, 2, userEmail)

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
                    finalMessage.append("For {}, Failed to access ROM file".format(debHostname) + "\n")
                    with open(os.path.join(configParentDir, "finalResults.txt"), 'w+') as results:
                        results.writelines(finalMessage)
                    changeFlag(jsonCfg, username, userProcNum, 2, userEmail)
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
                    finalMessage.append("For {}, Failed to access ROM file".format(debHostname) + "\n")
                    with open(os.path.join(configParentDir, "finalResults.txt"), 'w+') as results:
                        results.writelines(finalMessage)
                    changeFlag(jsonCfg, username, userProcNum, 2, userEmail)

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
                finalMessage.append("For {}, Failed to access MODS files".format(debHostname)+"\n")
                with open(os.path.join(configParentDir, "finalResults.txt"), 'w+') as results:
                    results.writelines(finalMessage)
                changeFlag(jsonCfg, username, userProcNum, 2, userEmail)

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
                finalMessage.append("For {}, Failed to access MODS files".format(debHostname) + "\n")
                with open(os.path.join(configParentDir, "finalResults.txt"), 'w+') as results:
                    results.writelines(finalMessage)
                changeFlag(jsonCfg, username, userProcNum, 2, userEmail)

    # connect to the test system
    try:
        systemID = int(jsonCfg["systemID"])
        debHostname = systems.objects.get(id=int(systemID)).debHostname
        debUsername = systems.objects.get(id=int(systemID)).debUsername
        debPassword = systems.objects.get(id=int(systemID)).debPassword
        debBootIndex = systems.objects.get(id=int(systemID)).debBootIndex
        winHostname = systems.objects.get(id=int(systemID)).winHostname
        winUsername = systems.objects.get(id=int(systemID)).winUsername
        winPassword = systems.objects.get(id=int(systemID)).winPassword
        winBootIndex = systems.objects.get(id=int(systemID)).winBootIndex
    except:
        finalMessage.append("System ID does not exist \n")
        with open(os.path.join(configParentDir, "finalResults.txt"), 'w+') as results:
            results.writelines(finalMessage)
        changeFlag(jsonCfg, username, userProcNum, 2, userEmail)

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=debHostname, username=debUsername, password=debPassword, port=22)
    except:
        finalMessage.append("Failed to connect to {}".format(debHostname) + "\n")
        with open(os.path.join(configParentDir, "finalResults.txt"), 'w+') as results:
            results.writelines(finalMessage)
        changeFlag(jsonCfg, username, userProcNum, 2, userEmail)

    sftp = ssh.open_sftp()

    #create cwd and baseDir
    try:
        ssh.exec_command("mkdir {}".format(jsonCfg["cwd"]))
        time.sleep(3)
        ssh.exec_command("mkdir {}".format(os.path.join(settings["testSystemBaseDir"], "automationLog", date)))
        time.sleep(2)
    except:
        finalMessage.append("Failed to create/access current working directory in the test system {}".format(debHostname) + "\n")
        with open(os.path.join(configParentDir, "finalResults.txt"), 'w+') as results:
            results.writelines(finalMessage)
        changeFlag(jsonCfg, username, userProcNum, 2, userEmail)

    if romPathList.len() == 0:
        romPathList.append("nullElement")

    for romPath in romPathList:
        shmooIndex = romPathList.index(romPath)
        romVersion = romVersionList[shmooIndex]
        if romPath == "nullElement" :
            pass
        else:
            #transfer the ROM
            try:
                with SCPClient(ssh.get_transport()) as scp:
                    scp.put(romPath, jsonCfg["cwd"])
            except:
                finalMessage.append("Failed to transfer ROM to {}".format(debHostname) + "\n")
                with open(os.path.join(configParentDir, "finalResults.txt"), 'w+') as results:
                    results.writelines(finalMessage)
                changeFlag(jsonCfg, username, userProcNum, 2, userEmail)

            if shmooIndex == 0:
                #transfer nvmt
                try:
                    with SCPClient(ssh.get_transport()) as scp:
                        scp.put(settings["nvmt"], jsonCfg["cwd"])
                except:
                    finalMessage.append("Failed to transfer NVMT to {}".format(debHostname) + "\n")
                    with open(os.path.join(configParentDir, "finalResults.txt"), 'w+') as results:
                        results.writelines(finalMessage)
                    changeFlag(jsonCfg, username, userProcNum, 2, userEmail)

                #transfer nvflash shell file
                try:
                    with SCPClient(ssh.get_transport()) as scp:
                        scp.put(os.path.join(baseDir,settings["testSystemFilesBaseDir"],"nvflash.sh"), jsonCfg["cwd"])
                except:
                    finalMessage.append("Failed to transfer test files to {}".format(debHostname) + "\n")
                    with open(os.path.join(configParentDir, "finalResults.txt"), 'w+') as results:
                        results.writelines(finalMessage)
                    changeFlag(jsonCfg, username, userProcNum, 2, userEmail)

            #Edit and start flashing
            fileObject = sftp.file(os.path.join(jsonCfg["cwd"],"nvflash.sh"), 'r+')
            testCommands = fileObject.readlines()
            fileObject.close()
            n = len(test_commands)
            testCommands[0] = "cd " + jsonCfg["cwd"] + "\n"
            testCommands[2] = "./nvflash_eng -A" + " " + romName
            for param in jsonCfg["vbiosFlash"]["params"]:
                testCommands[2] = testCommands[2] + " " + param
            testCommands[2] = testCommands[2] + " >> nvflash_" + romVersionList[shmooIndex] +  ".log\n"
            fileObject = sftp.file(os.path.join(jsonCfg["cwd"],"nvflash.sh"), 'w+')
            fileObject.writelines(testCommands)
            fileObject.close()

            # running the test
            testRunCommand = os.path.join(jsonCfg["cwd"],"nvflash.sh")
            ssh.exec_command(testRunCommand)
            time.sleep(30)

            #read nvflash.log and check if it flashed
            fileObject = sftp.file(os.path.join(jsonCfg["cwd"]),"nvflash_{}.log".format(romVersionList[shmooIndex]))
            logLines = fileObject.readlines()
            fileObject.close()
            errorKeywords = ["segmentation fault","mismatch","a system restart might be required","no nvidia test device found"]
            flashError = False
            for log in logLines:
                for keyword in errorKeywords:
                    if keyword.casefold() in log.casefold():
                        flashError = True

            #transfer nvflash.log
            copyNvflashCommand = "cp " + os.path.join(jsonCfg["cwd"], "nvflash_{}.log".format(romVersion)) + " " + os.path.join(settings["testSystemBaseDir"], "automationLog", date)
            ssh.exec_command(copyNvflashCommand)

            if flashError == True:
                finalMessage.append("Failed to flash {} on  {}".format(romVersionList[shmooIndex],debHostname) + "\n")
                with open(os.path.join(configParentDir, "finalResults.txt"), 'w+') as results:
                    results.writelines(finalMessage)
                changeFlag(jsonCfg, username, userProcNum, 2, userEmail)

        for modsPath in modsPathList:
            modsShmooIndex = modsPathList.index(modsPath)
            modsVersion = modsVersionList[modsShmooIndex]
            if shmooIndex == 0:
                if jsonCfg["modsTest"]["modsPresent"] == True:
                    pass
                else:
                    #transfer MODS to the CWD
                    try:
                        sftp.mkdir(os.path.join(jsonCfg["cwd"],modsVersion))
                        files = os.listdir(modsPath)
                        for file in files:
                            path = os.path.join(modsPath,file)
                            with SCPClient(ssh.get_transport()) as scp:
                                scp.put(path, os.path.join(jsonCfg["cwd"],modsVersion))
                    except:
                        finalMessage.append("Failed to transfer MODS to {}".format(debHostname) + "\n")
                        with open(os.path.join(configParentDir, "finalResults.txt"), 'w+') as results:
                            results.writelines(finalMessage)
                        changeFlag(jsonCfg, username, userProcNum, 2, userEmail)
                    # transfer extract.py to the test system
                    try:
                        with SCPClient(ssh.get_transport()) as scp:
                            scp.put(os.path.join(baseDir,settings["testSystemFilesBaseDir"],"extract.py"),settings["testSystemBaseDir"])
                    except:
                        finalMessage.append("Failed to transfer test files to {}".format(debHostname) + "\n")
                        with open(os.path.join(configParentDir, "finalResults.txt"), 'w+') as results:
                            results.writelines(finalMessage)
                        changeFlag(jsonCfg, username, userProcNum, 2, userEmail)

                    fileObject = sftp.file(os.path.join(settings["testSystemBaseDir"],"extract.py"), 'r+')
                    contents = fileObject.readlines()
                    contents[3] = "cwd = " + jsonCfg["cwd"] + "\n"
                    contents[4] = "modsVersion = " + modsVersion + "\n"
                    fileObject.close()
                    fileObject = sftp.file(os.path.join(settings["testSystemBaseDir"],"extract.py"), 'w+')
                    fileObject.writelines(contents)
                    fileObject.close()

                    ssh.exec_command('python3 ' + os.path.join(settings["testSystemBaseDir"],"extract.py"))

                #Run MODS Test

                #transfer shell file to the CWD and edit it
                try:
                    with SCPClient(ssh.get_transport()) as scp:
                        scp.put(os.path.join(baseDir, settings["testSystemFilesBaseDir"], "modsTest.sh"), os.path.join(jsonCfg["cwd"],modsVersion))
                except:
                    finalMessage.append("Failed to transfer test files to {}".format(debHostname) + "\n")
                    with open(os.path.join(configParentDir, "finalResults.txt"), 'w+') as results:
                        results.writelines(finalMessage)
                    changeFlag(jsonCfg, username, userProcNum, 2, userEmail)

                fileObject = sftp.file(os.path.join(jsonCfg["cwd"],modsVersion,"modsTest.sh"), 'r+')
                testCommands = fileObject.readlines()
                fileObject.close()
                testCommands[0] = "cd " + os.path.join(jsonCfg["cwd"],modsVersion) + "\n"
                if jsonCfg["modsTest"]["test"] == "modsInit":
                    testCommands[1] = "./mods mods.js " + jsonCfg["modsTest"]["arguments"]
                else:
                    testCommands[1] = "./mods gputest.jse -test " + jsonCfg["modsTest"]["test"] + " " + jsonCfg["modsTest"]["arguments"]
                fileObject = sftp.file(os.path.join(jsonCfg["cwd"], modsVersion, "modsTest.sh"), 'w+')
                fileObject.writelines(testCommands)
                fileObject.close()

            #Run MODS Test
            testRunCommand = os.path.join(jsonCfg["cwd"],modsVersion,"modsTest.sh")
            ssh.exec_command("mv " + os.path.join(jsonCfg["cwd"],modsVersion,"mods.log") + " " + os.path.join(jsonCfg["cwd"],modsVersion,"mods_prev.log"))
            time.sleep(3)
            ssh.exec_command(testRunCommand)

            #change the flag
            changeFlag(jsonCfg,username,userProcNum)

            files = sftp.listdir(os.path.join(jsonCfg["cwd"],modsVersion))
            modsExecuted = False
            lastToLastModified = 0
            while modsExecuted == False:
                time.sleep(60)
                if "mods.log" in files:
                    utime = sftp.stat(os.path.join(jsonCfg["cwd"],modsVersion,"mods.log")).st_mtime
                    lastModified = datetime.fromtimestamp(utime)
                    if last_modified == lastToLastModified:
                        modsExecuted = True
                    else:
                        lastToLastModified = lastModified
                else:
                    files = sftp.listdir(os.path.join(jsonCfg["cwd"],modsVersion))

            fileObject = sftp.file(os.path.join(jsonCfg["cwd"],modsVersion,"mods.log"), 'r+')
            contents = fileObject.readlines()
            notification = contents[len(contents) - 1]
            fileObject.close()
            error = False
            assertion = False
            if notification.startswith('MODS end'):
                for content in contents:
                    if content.startswith('Error'):
                        if "ModsDrvBreakPoint" in content:
                            assertion = True
                        if '000000000000' in content:
                            pass
                        else:
                            error = True
            else:
                for content in contents:
                    if "ModsDrvBreakPoint" in content:
                        assertion = True
                    elif content.startswith('Error'):
                        error = True
                    else:
                        error = True

                if assertion == True and error == False:
                    ssh.exec_command("killall -e mods")
                    changeFlag(jsonCfg, username, userProcNum, 1)
                    finalMessage.append("On {} MODS Test asserted for {} {}\n".format(debHostname,romVersion,modsVersion))
                elif assertion == False and error == False:
                    changeFlag(jsonCfg, username, userProcNum, 1)
                    finalMessage.append("On {} MODS Test passed for {} {}\n".format(debHostname, romVersion, modsVersion))
                elif assertion == False and error == True:
                    changeFlag(jsonCfg, username, userProcNum, 1)
                    finalMessage.append("On {} MODS Test failed for {} {}\n".format(debHostname, romVersion, modsVersion))

            copyModsCommand = "cp " + os.path.join(jsonCfg["cwd"],modsVersion,"mods.log") + " " + os.path.join(settings["testSystemBaseDir"],"automationLog",date,"mods_" + modsVersion +".log")
            ssh.exec_command(copyModsCommand)

    sftp.close()
    ssh.close()


procId = os.getpid()
finalMessage = []
print("reached pt1")
if __name__ == "__main__":
    print("reached pt2")
    username = sys.argv[1]
    userProcNum = sys.argv[2]
    userEmail = sys.argv[3]

    baseDir = Path(__file__).resolve().parent.parent

    settingsParentDir = os.path.join(baseDir, "settings")
    with open(os.path.join(settingsParentDir, "settings.json"), 'r') as json_file:
        settings = json.load(json_file)
    print("reached pt3")
    configParentPenDir = os.path.join(baseDir, "config_files")
    configParentDir = os.path.join(configParentPenDir,username,str(userProcNum))
    with open(os.path.join(configParentDir,"config.json"),'r') as json_file:
        jsonCfg = json.load(json_file)
    print("reached pt4")
    startTest(jsonCfg,settings,username,userProcNum,userEmail,configParentDir)
    print("reached pt5")
    with open(os.path.join(configParentDir,"finalResults.txt"),'w+') as results:
        results.writelines(finalMessage)

    changeFlag(jsonCfg, username, userProcNum, 2, userEmail)













