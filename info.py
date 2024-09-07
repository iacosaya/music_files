import os
import yaml

config_path = (__file__.replace(os.path.basename(__file__),'') + "config.yaml")
config = yaml.safe_load(open(config_path))

music_sort = {}
music_sort_count = {}
music_len = 0

album_files = (__file__.replace(os.path.basename(__file__),'') + "album_files.txt")
music_info = (__file__.replace(os.path.basename(__file__),'') + "music_info.txt")

sort_mode = 0

with open(album_files, "r+", encoding="utf8") as file:
    var_num_assign = 1
    for num, line in enumerate(list(file)):
        #add all lines that start with the ignore config setting to the dict "music_sort"
        if line.startswith(config["ignore"]):
            var_name = str(line.rstrip("\n")).lstrip(config["ignore"])
            music_sort[var_name] = var_num_assign
            var_num_assign += 1

with open(album_files, "r+", encoding="utf8") as file:
    for num, line in enumerate(list(file)):
        #add all lines that start with the ignore config setting to the dict "music_sort_count"
        if line.startswith(config["ignore"]):
            var_name = str(line.rstrip("\n")).lstrip(config["ignore"])
            music_sort_count[var_name] = 0

with open(album_files, "r+", encoding="utf8") as file:
    for line in file:
        line = line.lstrip(config["ignore"]).rstrip("\n")
        if line in music_sort:
            #change the sort mode based on the most sort line (one that starts with ignore config)
            sort_mode = music_sort[line]
        if line not in music_sort:
            try:
                if len(line) > 0:
                    music_sort_count[list(music_sort_count)[sort_mode - 1]] += 1
            except IndexError:
                print("No sort types found.")
                exit()
            if len(line) > 0:
                music_len += 1

def percentage(numerate, total):
    #generate a percentage
    return str((numerate / total) * 100)[:4]


with open(music_info, "w+", encoding="utf8") as file:
    for key, value in music_sort_count.items():
        #writes each sorting category to a text file called "music_info", with percentage info
        file.write(str(key) + ": "  + str(value) + "\n")
        try:
            file.write(f"Percentage: {str(percentage(value, music_len))}%")
        except ZeroDivisionError:
            print("No albums found.")
            exit()
        if list(music_sort_count).index(key) != len(music_sort_count) - 1:
            file.write("\n\n")
