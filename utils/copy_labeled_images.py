from glob import glob
from os import path
from shutil import copyfile

# Directories for src and dst papths
DATA_DIR = "./official-emergency/emergency/"
OUTPUT_DIR = "./labeledImages/"
# label files
files = glob(DATA_DIR+"*.xml")

for file in files:
    # names to create src and dst
    basename = path.basename(file)
    filename = basename.split(".")[0]
    imageFile = filename + ".jpg"
    # copying files 
    copyfile(DATA_DIR+imageFile, OUTPUT_DIR+imageFile)
    print(f"{imageFile} copied!")
    copyfile(DATA_DIR+basename, OUTPUT_DIR+basename)
    print(f"{basename} copied!")
    
print("FINISHED!")
