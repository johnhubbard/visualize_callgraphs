# visualize_callgraphs
This is a python-graphviz script that reads in a .json file that describes
which functions call which other functions, and generates a corresponding
.png image that shows that diagram.

In order to get the right Python Graphviz support to be able to run this script,
here are a (very few!) examples of installation steps on various systems:

On Arch Linux:
	sudo pacman -S python-graphviz

On Ubuntu Linux:
	sudo apt install python3-graphviz

Examples:

	make
	make d=1              # Display the resulting .png image in a browser
	make basic_example
	make follow_page d=1

Or, if you add your_diagram.py, the Makefile will pick it up automatically, so:

	make your_diagram d=1
