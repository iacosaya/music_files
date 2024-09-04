# Music Files v0.3
Repository for mass reading of music folders and subfolders.

# BASIC GUIDE

1. Download the code as a .zip file (will add a release version in later developement potentially)

2. Edit config.yaml to your liking, instructions on configurations are inside the file.

3. When done, run the batch file "run.bat."

Add any albums that are you want the program to skip to "ignore.txt", seperated by on newlines.

# INFO
music_list.py is the main program which creates the following text files:
- album_files.txt
-   Creates a file containing all the titles and album artists in your directory
- music_files.txt
-   Creates a file containing all possible roots, directories, etc. inside the main directory

info.py is a optional program which creates the follow text files:
- music_info
-   Creates a file containing all sort modes, are created within album_files with any newlines that start with the ignore config setting
-   In example, with the default configuration, any new line starting with -- (like --Owned albums) will be added as a sort mode, and printed to the text file
