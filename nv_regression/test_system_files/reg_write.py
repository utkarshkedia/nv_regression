import subprocess,sys,time,os

reg_list = ['0x009a0890']
reg_dict = {'0x009a0890': '0xEE213F88'}


if "win" in sys.platform:
    for reg in reg_list:
        a=subprocess.Popen(["nvpex2.exe", "-b", "01:00.0", "-r", "W:0:"+reg+":"+reg_dict[reg]])
        a.wait()
else:
    for reg in reg_list:
        os.system("nvpex2 -b 01:00.0 -r W:0:"+reg+":"+reg_dict[reg])
	time.sleep(1)
    
       
        
