# Created by John Hubbard, January, 2022
#
# Usage:
#       1) Create .json files that describe connectivity between items, such as
#          callers and callees of subroutines in a program that you're trying to
#          understand (or document).
#
#       2) This Makefile does not need to be modified. It will pick up the
#          *.json files and build and optionally (via "make d=1") display the
#          corresponding *.png images.
# Examples:
#	  make
#	  make d=1              # Display the resulting .png image in a browser
#	  make basic_example
#	  make follow_page d=1

SOURCES  := $(wildcard *.json)
IMAGES   := $(patsubst %.json,%.png,$(SOURCES))
DIAGRAMS := $(patsubst %.json,%,$(SOURCES))

d ?=
DISPLAY_PROGRAM ?= firefox

all: $(DIAGRAMS)
	
# Allow typing the short form, such as "make basic_example", by generating
# a rule for each diagram that translates each diagram name into its
# corresponding image (file) name:
define create-diagram-rules
$1: $1.png
	$(if $(d),$(DISPLAY_PROGRAM) $1.png,)
endef

$(foreach diagram,$(DIAGRAMS),$(eval $(call create-diagram-rules,$(diagram))))

%.png: generate_diagram.py %.json
	python3 $^

# The newer ("import graphviz") library leaves behind the $(DIAGRAMS) files,
# in addition to the *.png IMAGES, so clean those up as well:
clean:
	rm $(IMAGES) $(DIAGRAMS)

.PHONY: clean $(DIAGRAMS)
