#!/usr/bin/env python3

from time import sleep
import sys
from collections import OrderedDict
from os.path import join
from json import loads, dumps

source = "src"
src = "theme.json"
dst = "theme2.json"

data = OrderedDict({"elements": OrderedDict(), "colors": {}, "modes": {}})

with open(join(source, src), "r") as f:
    data_parsed = loads(f.read(), object_pairs_hook=OrderedDict)

# Elements
# Set default value for non-set elements:
for element, config in data_parsed["elements"].items():
    if "separator" in element:
        data["elements"][element] = "---"
        continue

    data["elements"][element] = {
        "description": data_parsed["elements"][element],
    }

# Colors
for color, value in data_parsed["colors"].items():
    data["colors"][color] = value["color"]
    for element in value["elements"]:
        data["elements"][element]["color"] = color

# Mode
for mode, value in data_parsed["modes"].items():
    data["modes"][mode] = value["mode"]
    for element in value["elements"]:
        data["elements"][element]["mode"] = mode

# Apply checkbox logic
for element in data_parsed["check"]:
    data["elements"][element]["checked"] = True

with open(join(source, dst), "w") as f:
    f.write(dumps(OrderedDict(data), indent=4))
