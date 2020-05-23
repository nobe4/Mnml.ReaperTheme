#!/usr/bin/env python3

import os

src = "src/images/"
dst = "../Mnml/"

src_files = [
    os.path.join(dp, f)[len(src) :]
    for dp, dn, filenames in os.walk(src)
    for f in filenames
]
dst_files = [
    os.path.join(dp, f)[len(dst) :]
    for dp, dn, filenames in os.walk(dst)
    for f in filenames
]

print("len src {}".format(len(src_files)))
print("len dst {}".format(len(dst_files)))

print("\nFiles in src but not dst")
for file in src_files:
    if file not in dst_files:
        print(file)

print("\nFiles in dst but not src")
for file in dst_files:
    if file not in src_files:
        print(file)
