# Created by John Hubbard, January, 2022
#
# Usage:
#
#       1) Create python scripts that generate .png files of the same name.
#          For example, use Python's GraphViz: "import gv".
#
#       2) This Makefile does not need to be modified. It will pick up the
#          *.py files and build and optionally (via "make d=1") display the
#          corresponding *.png images.
#
#       3) Examples, assuming that you have follow_page.py:
#
#       make
#       make d=1              # Display the resulting .png image in a browser
#       make follow_page
#       make follow_page.png  # Same result as previous
#       make follow_page d=1

SOURCES  := $(wildcard *.py)
IMAGES   := $(patsubst %.py,%.png,$(SOURCES))
DIAGRAMS := $(patsubst %.py,%,$(SOURCES))

d ?=
DISPLAY_PROGRAM ?= firefox

all: $(DIAGRAMS)
	
# Allow typing the short form, such as "make bio_release_pages", by generating 
# a rule for each diagram that translates each diagram name into its
# corresponding image (file) name:
define create-diagram-rules
$1: $1.png
	$(if $(d),$(DISPLAY_PROGRAM) $1.png,)
endef

$(foreach diagram,$(DIAGRAMS),$(eval $(call create-diagram-rules,$(diagram))))

%.png: %.py
	python3 $<

# The newer ("import graphviz") library leaves behind the $(DIAGRAMS) files,
# in addition to the *.png IMAGES, so clean those up as well:
clean:
	rm $(IMAGES) $(DIAGRAMS)

.PHONY: clean $(DIAGRAMS)
