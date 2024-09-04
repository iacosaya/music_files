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

#creates the files neccesary in the directory of the .py file
music_files = (__file__.replace(os.path.basename(__file__),'') + "music_files.txt")
album_files = (__file__.replace(os.path.basename(__file__),'') + "album_files.txt")
try:
    desktop = pathlib.Path(config["directory"])
except TypeError:
    print("Directory not set.")
    exit()
with open(music_files, mode="w", encoding="utf8") as m_file:
    for music in list(desktop.rglob("*")):
        m_file.write(str(music) + "\n")

for root, dirs, files in os.walk(config["directory"]):
    for file in files:
        #adds each root which contains music files inside of it
        if file.endswith(tuple(file_types)):
            album_files_list.append(root)

for n, album_name in enumerate(album_files_list):
    if config["album_dir"] == "triple":
        if album_files_list[n-1] != album_name:
            album_name = str(album_name).split("\\")
            del album_name [:-3]
            del album_name [2]
            if config["order"] == "artist":
                album_name = str(album_name[0]) + " - " + str(album_name[1])
                new_files_list.append(album_name)
            elif config["order"] == "album":
                album_name = str(album_name[1]) + " - " + str(album_name[0])
                new_files_list.append(album_name)

    elif config["album_dir"] == "double":
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
            else:
                print("Album sort mode not set.")
                exit()

    elif config["album_dir"] == "single":
        if album_files_list[n-1] != album_name:
            #splits the address into a list, split with \
            album_name = str(album_name).split("\\")
            del album_name [:-1]
            album_name = ''.join(album_name)
            new_files_list.append(album_name)
    
    else:
        print("Album directory mode not set.")
        exit()

#sorts the list alphabetically (which i think is already done but idc)
new_files_list.sort()
#creates a copy of the newfilelist so it doesn't mess up code
new_file_list_copy = new_files_list[:]
new_file_list_data = new_files_list[:]

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
    for index_n in new_files_list:
        if index_n != len(new_files_list):
            file.write(index_n + "\n")
        else:
            file.write(index_n)

with open(album_files, "r", encoding="utf8") as file:
    #reads all the lines in the file
    data = file.readlines()

for line in data[:]:
    if line.rstrip("\n") not in new_file_list_data:
        if (line[:2] == config["ignore"]) or (line.strip() == ""):
            ""
        elif line in ignore_list:
            ""
        else:
            #removes any lines that DON'T start with ignore config from the text file
            data.remove(line)

with open(album_files, 'w', encoding='utf8') as file: 
    file.writelines(data)
