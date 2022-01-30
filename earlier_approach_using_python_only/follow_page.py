#!/usr/bin/env python3
# Created by John Hubbard, January, 2022
#
# Creates a .png image that shows call paths; in this case, those callpaths
# related to the Linux kernel's follow_page() routine.
#
# See https://graphviz.readthedocs.io/en/stable/examples.html
#     https://www.w3schools.com/colors/colors_hexadecimal.asp

import graphviz
from pathlib import Path

# Use this script's file name (changing .py to .png) for the output image file.
# The .png is added by graphviz.Digraph(), not here:
base_filename = Path(__file__).stem

g = graphviz.Digraph(filename=base_filename, format="png",
                     node_attr={"color": "black", "fillcolor": "#b5b5ff",
                     "style": "filled"})

def connect(from_node, to_node):
    g.edge(from_node, to_node)

def set_color(node, color):
    g.node(node, fillcolor=color)

HIGHLIGHT_COLOR = "yellow"
TO_DELETE_COLOR = "deeppink"

set_color("follow_pfn_pte", HIGHLIGHT_COLOR)
connect("follow_page_pte", "follow_pfn_pte")

connect("follow_page", "follow_page_mask")
connect("__get_user_pages", "follow_page_mask")
connect("follow_page_mask", "follow_p4d_mask")
connect("follow_p4d_mask", "follow_pud_mask")
connect("follow_pud_mask", "follow_pmd_mask")
connect("follow_pmd_mask", "follow_page_pte")
connect("follow_pmd_mask", "follow_trans_huge_pmd")

follow_page_callers = \
    "munlock_vma_pages_range\n" + \
    "do_pages_stat_array (migrate.c)\n" + \
    "add_page_for_migration (migrate.c)\n" + \
    "split_huge_pages_pid\n" + \
    "scan_get_next_rmap_item (ksm)\n" + \
    "get_mergeable_page (ksm)\n" + \
    "break_ksm (ksm)\n" + \
    "gmap_make_secure (s390)\n" + \
    "do_secure_storage_access (s390)\n"

connect(follow_page_callers, "follow_page")

connect("__get_user_pages_locked", "__get_user_pages")
connect("populate_vma_page_range", "__get_user_pages")
connect("faultin_vma_page_range", "__get_user_pages")

__get_user_pages_locked_callers = [
    "pin_user_pages_locked",
    "get_user_pages_unlocked",
    "get_user_pages_locked",
    "__get_user_pages_remote",
    "__gup_longterm_locked",
    "get_dump_page",
    "fault_in_safe_writeable",
    ]

for caller in __get_user_pages_locked_callers:
    connect(caller, "__get_user_pages_locked")

connect("-- NO CALLERS --", "pin_user_pages_locked")
connect("lookup_node", "get_user_pages_locked")

connect("pin_user_pages", "__gup_longterm_locked")
connect("get_user_pages", "__gup_longterm_locked")
connect("__gup_longterm_unlocked", "__gup_longterm_locked")
connect("__get_user_pages_remote", "__gup_longterm_locked")

connect("internal_get_user_pages_fast", "__gup_longterm_unlocked")

connect("pin_user_pages_fast", "internal_get_user_pages_fast")
connect("pin_user_pages_fast_only", "internal_get_user_pages_fast")
connect("get_user_pages_fast", "internal_get_user_pages_fast")
connect("get_user_pages_fast_only", "internal_get_user_pages_fast")

set_color("pin_user_pages_locked", TO_DELETE_COLOR)
set_color("get_user_pages_locked", TO_DELETE_COLOR)

connect
g.render()

