#!/usr/bin/env python3
# vim: tabstop=4:expandtab:shiftwidth=4:autoindent

import re
import time
import os
import math
import shutil
import zipfile
from jinja2 import Environment, FileSystemLoader

# Colors
colors = {
    "null": "ff33cc",
    "black": "353535",
    "black_l": "8e8277",
    "white": "c9bba3",
    "white_l": "efe1bf",
    "red": "d73925",
    "red_l": "fe6142",
    "green": "a8a521",
    "green_l": "c4c431",
    "yellow": "dfa82a",
    "yellow_l": "fcc73c",
    "blue": "549699",
    "blue_l": "94b3a8",
    "magenta": "bf7897",
    "magenta_l": "dc9aab",
    "cyan": "79aa7d",
    "cyan_l": "9dc98e",
}

# Conv color from regrbl to red+green*256+blue*256*256
def hexToCol(color):
    red = int(color[0:2], 16)
    green = int(color[2:4], 16) * 256
    blue = int(color[4:6], 16) * 256 * 256
    return str(red + green + blue)


# int = red + green*256 + blue*256*256
# red / 256 < 1
# green / (256 * 256) < 1
# blue / (256 * 256 * 256) < 1


def colToRGB(color):
    color = int(color)
    red = color - math.floor(color / 256) * 256
    color = math.ceil((color - red) / 256)
    green = color - math.floor(color / 256) * 256
    color = math.ceil((color - red) / 256)
    blue = color - int(color / 256) * 256
    return red, green, blue


def rgbToCol(r, g, b):
    return int(r) + int(g) * 256 + int(b) * 256 * 256


def active(color):
    return str(int(color) - 2147483648)


def draw_mode(type, value):
    base = {
        "normal": [
            "9568256",
            "9574656",
            "9581056",
            "9587712",
            "9594368",
            "9601024",
            "9607424",
            "9614080",
            "9620480",
            "9627136",
            "9633792",
        ],
        "add": [
            "9568257",
            "9574657",
            "9581313",
            "9587713",
            "9594369",
            "9601025",
            "9607425",
            "9614081",
            "9620481",
            "9627137",
            "9633793",
        ],
    }

    # Original calculation method, which doesn't work
    # value = base[type] + int((2**16) * value)
    return base[type][value]


# Load the template
env = Environment(loader=FileSystemLoader(searchpath="."))

# Convert the colors
for color in colors:
    colors[color] = hexToCol(colors[color])


def light(color, amount):
    r, g, b = colToRGB(color)

    if abs(amount) > 100:
        print("too much light: {}".format(amount))
        return r, g, b

    alpha = amount / 100

    if alpha < 0:
        alpha += 1
        r *= alpha
        g *= alpha
        b *= alpha
    else:
        r = (255 - r) * alpha + r
        g = (255 - g) * alpha + g
        b = (255 - b) * alpha + b

    return rgbToCol(r, g, b)


# Custom values for settings stuff up
env.filters["active"] = active
env.filters["light"] = light
env.globals["draw_mode"] = draw_mode

# Cleanup the dest folder
shutil.rmtree("dest/assets", ignore_errors=True)

# Copy the assets into the dest folder
shutil.copytree("assets", "dest/assets")

# Compile and write the templates
print("Generate and write ReaperTheme")
theme = env.get_template("Mnml.ReaperTheme.jinja")
theme = theme.render(colors)
with open("dest/Mnml.ReaperTheme", "w") as f:
    f.write(theme)

print("Generate and write rtconfig")
rtconfig = env.get_template("rtconfig.txt.jinja")
rtconfig = rtconfig.render(colors)
with open("dest/assets/rtconfig.txt", "w") as f:
    f.write(rtconfig)

# Create a zip archive of the dest folder
print("Generate and write zip file")
shutil.make_archive("Mnml", "zip", "dest")
shutil.move("Mnml.zip", "../Mnml{}.ReaperThemeZip".format(time.time()))
