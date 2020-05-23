#!/usr/bin/env python3
from PIL import Image
from os.path import join
from os import makedirs
from shutil import copyfile, copytree, rmtree
import json

destination = ".."
source = "src"
theme = "Mnml.ReaperTheme"
rtconfig = "rtconfig.txt"
dir_img = join(destination, "Mnml")
dir_150 = join(dir_img, "150")
dir_200 = join(dir_img, "200")

ratio_200_150 = 0.75
ratio_200_100 = 0.5
ratio_150_100 = 0.66

# Create the assets folders
try:
    rmtree(dir_img)
except:
    pass

makedirs(dir_img)
makedirs(dir_200)
makedirs(dir_150)

# Copy the theme into destination
copyfile(join(source, theme), join(destination, theme))
copyfile(join(source, rtconfig), join(dir_img, rtconfig))

# Read data file
with open("combined.json", "r") as f:
    data = json.loads(f.read())

# Read combined image
img = Image.open("combined.png")


parts = data["parts"]

for name in parts:
    part = parts[name]

    # Crop each image
    part_cropped = img.crop(
        (part["x"], part["y"], part["x"] + part["w"], part["y"] + part["h"],)
    )

    # Save only in the img dir
    part_cropped.save(join(dir_img, name))
