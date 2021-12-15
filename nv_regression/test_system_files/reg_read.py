import subprocess,sys,csv

test_system_directory = "C:\\Users\\lab\\Automation"
autochar_directory = "D:\\tmp\\PowerScripts\\Autochar"
reg_list = ['0x009a0890']
reg_list = ['0x009a0890', '0x009A0898']
reg_values=[]
reg_dict={}

if "win" in sys.platform:
    for reg in reg_list:
        a=subprocess.Popen(["nvpex2.exe", "-b", "01:00.0", "-r", "R:0:"+reg], stdout=subprocess.PIPE)
        output,errors = a.communicate()
        a.wait()
        reg_dict[reg]="0x"+output[output.index('#')+2:output.index('#')+10]
        reg_values.append("0x"+output[output.index('#')+2:output.index('#')+10])

else:
    for reg in reg_list:
        a=subprocess.Popen(["nvpex2", "-b", "01:00.0", "-r", "R:0:"+reg], stdout=subprocess.PIPE)
        output,errors = a.communicate()
        a.wait()
        reg_dict[reg]="0x"+output[output.index('#')+2:output.index('#')+10]
        reg_values.append("0x"+output[output.index('#')+2:output.index('#')+10])
    

with open(autochar_directory + "\\reg_writeback.py","r+") as f:
    contents=f.readlines()
    
contents[2] = "reg_list = " + str(reg_list) + "\n"
contents[3] = "reg_values = " + str(reg_values) + "\n"
contents[4] = "reg_dict = " + str(reg_dict) + "\n"

with open(autochar_directory + "\\reg_writeback.py","w+") as f:
    f.writelines(contents)
    
 
