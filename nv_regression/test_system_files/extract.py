import os
import tarfile
files=os.listdir('/mnt/storage/mods')
mtime=0
for file in files:
    path='/mnt/storage/mods'+ '/' + file
    if os.path.getmtime(path) > mtime:
        mtime = os.path.getmtime(path)
        Mods_path = path
        Mods_file = file

files=os.listdir(Mods_path)
for file in files:
    if file.endswith(".tgz") or file.endswith(".gz"):
        my_tar = tarfile.open(Mods_path + '/' + file)
        my_tar.extractall(Mods_path) # specify which folder to extract to
        my_tar.close()
