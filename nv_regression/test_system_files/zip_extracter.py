from zipfile import ZipFile
import argparse

driver_targetLoc = "D:\\Drivers"

parser = argparse.ArgumentParser()
parser.add_argument('--driver_file',type=str,required=True)
args = parser.parse_args()
driver_file = args.driver_file
path = driver_targetLoc + "\\" + driver_file
with ZipFile(path + "\\IS.zip",'r') as zipObj:
    zipObj.extractall(path)
    
