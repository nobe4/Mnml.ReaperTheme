#!/usr/bin/env python3

from PIL import Image
from os import listdir
from sys import exit
from os.path import isfile, join
from collections import OrderedDict
import json

group_per_line = 3
padding = 1
src = "src/images"
dst = "."

files = OrderedDict()

for f in listdir(join(src, "200")):
    if isfile(join(src, "200", f)):
        files[f] = ["200"]

for f in listdir(join(src, "150")):
    if isfile(join(src, "150", f)):
        if f not in files:
            files[f] = []
        files[f].append("150")

for f in listdir(src):
    if isfile(join(src, f)):
        if f not in files:
            files[f] = []
        files[f].append("100")

# Some data to keep track of positions
currentPos = [0, 0]
maxHeight = 0
maxWidth = 0

# Exported data
data = {
    # Full result size
    "w": 0,
    "h": 0,
    # List of all parts
    "parts": {},
}

# Loop 1: preparing the result.
for file in files:
    currentPos = [0, maxHeight]

    for folder in files[file]:
        filename = join(folder if folder != "100" else "", file)

        img = Image.open(join(src, filename))

        # Save position and file.
        data["parts"][filename] = {
            "x": currentPos[0],
            "y": currentPos[1],
            "w": img.size[0],
            "h": img.size[1],
        }

        # Update position
        currentPos[0] += img.size[0] + padding
        tmpNextLine = currentPos[1] + img.size[1]

        if tmpNextLine > maxHeight:
            maxHeight = tmpNextLine + padding

        if currentPos[0] > maxWidth:
            maxWidth = currentPos[0]

data["w"] = maxWidth
data["h"] = maxHeight

# Save the json representation of the image.
with open("combined.json", "w") as f:
    json.dump(data, f, indent=4, sort_keys=True)

# Create result image.
result = Image.new("RGBA", (data["w"], data["h"]), (255, 0, 0, 0))

# Loop 2: add each part into the result.
for filename in data["parts"]:
    img = Image.open(join(src, filename))
    result.paste(img, (data["parts"][filename]["x"], data["parts"][filename]["y"]))

result.save("combined.png")
