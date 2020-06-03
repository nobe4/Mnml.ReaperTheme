#!/usr/bin/env python3

from time import sleep
import sys
from shutil import copyfile, copytree, rmtree
from os.path import join
from jinja2 import Template
from json import loads, dumps

destination = ".."
source = "src"
rtconfig = "rtconfig.txt"
template = "Mnml.ReaperTheme.jinja"
theme = "Mnml.ReaperTheme"
data = "theme.json"

dir_img = join(destination, "Mnml")


def render_theme():
    # Load data from the theme
    with open(join(source, data), "r") as f:
        data_parsed = loads(f.read())

    # Compute the elements in the data
    for color, value in data_parsed["colors"].items():
        for element in value["elements"]:
            data_parsed["elements"][element] = {
                "color": str(int(value["color"], 16)),
                "description": data_parsed["elements"][element],
            }

    # Set default value for non-set elements:
    for element, config in data_parsed["elements"].items():
        if config == "TODO":
            data_parsed["elements"][element] = {
                "color": "0",
                "description": data_parsed["elements"][element],
            }

    with open(join(source, template), "r") as f:
        t = Template(f.read())

    with open(join(destination, theme), "w") as f:
        f.write(t.render(data_parsed))


while True:
    try:
        copyfile(join(source, rtconfig), join(dir_img, rtconfig))
        render_theme()
    except Exception as ex:
        print(ex)
    sleep(3)
