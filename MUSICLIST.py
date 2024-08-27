import pathlib
from pathlib import Path
import os
import yaml

config_path = (__file__.replace(os.path.basename(__file__),'') + "config.yaml")
config = yaml.safe_load(open(config_path))

#imports the list of ignored albums (from ignore.txt)
ignore = (__file__.replace(os.path.basename(__file__),'') + "ignore.txt")

album_files_list = []
new_files_list = []

#the file types the program searches for
file_types = config["file_types"]

#albums that the program picks up that you want to ignore
ignore_list = []
with open(ignore, mode="r", encoding="utf8") as file:
    for i_scan in file:
        ignore_list.append(i_scan.rstrip("\n"))

print(ignore_list)

#creates the files neccesary in the directory of the .py file
music_files = (__file__.replace(os.path.basename(__file__),'') + "music_files.txt")
album_files = (__file__.replace(os.path.basename(__file__),'') + "album_files.txt")

desktop = pathlib.Path(config["directory"])
with open(music_files, mode="w", encoding="utf8") as m_file:
    for music in list(desktop.rglob("*")):
        m_file.write(str(music) + "\n")

for root, dirs, files in os.walk(config["directory"]):
    for file in files:
        if file.endswith(tuple(file_types)):
            album_files_list.append(root)

for n, album_name in enumerate(album_files_list):
    if config["album_dir"] == "double":
        if album_files_list[n-1] != album_name:
            #splits the address into a list, split with \
            album_name = str(album_name).split("\\")
            del album_name [:-2]
            #if you want albums sorted by ARTIST | ALBUM switch the numbers around
            if config["order"] == "artist":
                album_name = str(album_name[0]) + " - " + str(album_name[1])
                new_files_list.append(album_name)
            elif config["order"] == "album":
                album_name = str(album_name[1]) + " - " + str(album_name[0])
                new_files_list.append(album_name)
    elif config["album_dir"] == "single":
        if album_files_list[n-1] != album_name:
            #splits the address into a list, split with \
            album_name = str(album_name).split("\\")
            del album_name [:-1]
            album_name = ''.join(album_name)
            new_files_list.append(album_name)

#sorts the list alphabetically (which i think is already done but idc)
new_files_list.sort()
#creates a copy of the newfilelist so it doesn't mess up code
new_file_list_copy = new_files_list[:]

for item_remove in new_file_list_copy:
    if str(item_remove) in ignore_list:
        new_files_list.remove(item_remove)

try:
    open(album_files, encoding="utf8")
except FileNotFoundError:
    open(album_files, "x", encoding="utf8")

with open(album_files, "r+", encoding="utf8") as file:
    for index_x in file:
        index_x = index_x.rstrip("\n")
        if index_x in new_files_list:
            #removes items from the list if they are already contained within album_files.txt
            new_files_list.remove(index_x)

with open(album_files, "a+", encoding="utf8") as file:
    if (len(new_files_list) >= 1):
        file.write("\n")
    for index_n in new_files_list:
        file.write(index_n + "\n")
