import os
import tarfile
connector = "/"
cwd = "/mnt/storage/mods"
modsVersion = ""
modsPath = connector.join((cwd, modsVersion))
files=os.listdir(modsPath)
for file in files:
    if file.endswith(".tgz") or file.endswith(".gz"):
        my_tar = tarfile.open(modsPath + '/' + file)
        my_tar.extractall(modsPath) # specify which folder to extract to
        my_tar.close()
