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

template_data = {"elements": {}}


def render_theme():
    # Load data from the theme
    with open(join(source, data), "r") as f:
        data_parsed = loads(f.read())
        elements = data_parsed["elements"]
        modes = data_parsed["modes"]
        colors = data_parsed["colors"]
        template_data["fonts"] = data_parsed["fonts"]

    for name, element in elements.items():
        if "separator" in name:
            continue

        template_data["elements"][name] = {"description": element["description"]}

        if element.get("color", False):
            value = int(colors[element["color"]], 16)

            if element.get("checked", False):
                value = -2147483648 + value

            template_data["elements"][name]["value"] = value

        elif element.get("mode", False):
            template_data["elements"][name]["value"] = modes[element["mode"]]

    with open(join(source, template), "r") as f:
        t = Template(f.read())

    with open(join(destination, theme), "w") as f:
        f.write(t.render(template_data))


while True:
    try:
        copyfile(join(source, rtconfig), join(dir_img, rtconfig))
        render_theme()
    except Exception as ex:
        print(ex)
    sleep(3)
