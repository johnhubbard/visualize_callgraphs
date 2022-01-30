#!/usr/bin/env python3
#
# Creates a .png image that shows call paths.
#
# Usage: generate_diagram.py <input-file.json>
#
# See example.json for supported key words and their use.
#
# See https://graphviz.readthedocs.io/en/stable/examples.html
#     https://www.w3schools.com/colors/colors_hexadecimal.asp

import graphviz
import json
import sys
import os
from pathlib import Path

# Use the input filename (changing .json to .png) for the output image file.
# The .png is added by graphviz.Digraph(), not here:
json_filename = str(sys.argv[1])
base_filename = os.path.splitext(json_filename)[0]

g = graphviz.Digraph(filename=base_filename, format="png",
                     node_attr={"color": "black", "fillcolor": "#b5b5ff",
                     "style": "filled"})

def connect(from_node, to_node):
    g.edge(from_node, to_node)

def set_color(node, color):
    g.node(node, fillcolor=color)

f = open(json_filename)
data = json.load(f)

# TODO: check for existence instead of catching exceptions, duh.
for item in data["items"]:
    try:
        connect(item["name"], item["child"])
    except Exception as e:
        pass

    try:
        connect(item["parent"], item["name"])
    except Exception as e:
        pass

    try:
        for parent in item["parents"]:
            connect(parent, item["name"])
    except Exception as e:
        pass

    try:
        for child in item["children"]:
            connect(item["name"], child)
    except Exception as e:
        pass

    try:
        set_color(item["name"], item["color"])
    except Exception as e:
        pass

g.render()

