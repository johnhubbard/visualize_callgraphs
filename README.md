# visualize_callgraphs
This is a python-graphviz script that describes which functions call which
other functions, and generates a corresponding .png image that shows that
diagram.

Examples:

	make
	make d=1              # Display the resulting .png image in a browser
	make follow_page
	make follow_page.png  # Same result as previous
	make follow_page d=1

Or, if you add your_diagram.py, the Makefile will pick it up automatically, so:

	make your_diagram d=1
