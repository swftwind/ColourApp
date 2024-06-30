# initial commit for main.py

# test
# test 2

print("zamn zawg")


import tkinter as tk

''' TKInter is a standard inferface and gui library that we will be using to create windows, buttons, dipsplay photos, and mostly anything to do
    with human interaction with the code.'''

import os
from tkinter import Toplevel, Listbox, Scrollbar, Frame
from tkinter import filedialog
from screen_selector import make_selection # I don't know how much experience you have with linking code from file to file, but here we are just
                                           # taking the function from screen_selector.py and using it with the following environment below.
                                           # This was done for code organizational purposes.
from file_veiwer import open_selections

# Create the main Tkinter window that users will a button on.
root = tk.Tk() # The root variable refers to the main window of the application, ex. the window with the botton in it.
root.title("Selection Tool")
root.geometry("300x100")

# Variable for (constant) button width
button_width = 15

# Add the 'make selection' button
new_selection_button = tk.Button(root, text="Make Selection", width=button_width, command=lambda: make_selection(root))
# The lambda function acts as a wrapper for the make_selection function which occurs on button press.

# Alter whitespace padding to ensure button visibility.
new_selection_button.pack(anchor='nw', pady=10, padx=10)

# Add the 'open selections' button
open_selections_button = tk.Button(root, text="Open Selections", width=button_width, command=lambda: open_selections(root))
# This button will open a file dialog to select a directory and display saved selections.
# It also uses a lambda function as tk root object data needs to be handed to file_veiwer.py to allow
# drawing and access to the common canvases created by this file.

# Alter whitespace padding to ensure button visibility.
open_selections_button.pack(anchor='nw', pady=0, padx=10)

# Start the Tkinter event loop. This waits for 'events' (such as mouse clicks or key presses) after which these events can be mapped to functionality.
root.mainloop()