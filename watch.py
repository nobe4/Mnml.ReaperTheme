#!/usr/bin/env python3

from time import sleep
from shutil import copyfile, copytree, rmtree
from os.path import join

destination = ".."
source = "src"
rtconfig = "rtconfig.txt"

dir_img = join(destination, "Mnml")


while True:
    try:
        copyfile(join(source, rtconfig), join(dir_img, rtconfig))
    except:
        pass
    sleep(3)
