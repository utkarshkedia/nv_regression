import os
import tarfile

cwd = "/mnt/storage/mods"
modsVersion = ""
modsPath = os.path.join(cwd + modsVersion)
files=os.listdir(modsPath)
for file in files:
    if file.endswith(".tgz") or file.endswith(".gz"):
        my_tar = tarfile.open(Mods_path + '/' + file)
        my_tar.extractall(Mods_path) # specify which folder to extract to
        my_tar.close()
