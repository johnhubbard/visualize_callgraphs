#!/usr/bin/env python3
# Created by John Hubbard, Jan, 2022
#
# Creates a .png image that shows call paths.
#
# Usage: generate_diagram.py <input-file.json>
#
# See basic_example.json and the README.md, for supported key words and their
# use.
#
# See https://graphviz.readthedocs.io/en/stable/examples.html
#     https://www.w3schools.com/colors/colors_hexadecimal.asp

import graphviz
import json
import sys
import os
from pathlib import Path

if len(sys.argv) != 2:
    print("Usage:\n\n    %s <input-filename>\n" % str(sys.argv[0]))
    print("Example:\n\n    %s basic_example.json\n" % str(sys.argv[0]))
    exit(1)

# Use the input filename (changing .json to .png) for the output image file.
# The .png is added by graphviz.Digraph(), not here:
json_filename = str(sys.argv[1])
base_filename = os.path.splitext(json_filename)[0]

g = graphviz.Digraph(filename=base_filename, format="png",
                     node_attr={"color": "black", "fillcolor": "lightblue",
                     "style": "filled"})

def connect(from_node, to_node):
    g.edge(from_node, to_node)

def set_color(node, color):
    g.node(node, fillcolor=color)

f = open(json_filename)
data = json.load(f)

for item in data["items"]:
    if "child" in item:
        connect(item["name"], item["child"])

    if "children" in item:
        for child in item["children"]:
            connect(item["name"], child)

    if "parent" in item:
        connect(item["parent"], item["name"])

    if "parents" in item:
        for parent in item["parents"]:
            connect(parent, item["name"])

    if "color" in item:
        set_color(item["name"], item["color"])

g.render()

