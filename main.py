# initial commit for main.py

# test
# test 2

print("zamn zawg")


import tkinter as tk

''' TKInter is a standard inferface and gui library that we will be using to create windows, buttons, dipsplay photos, and mostly anything to do
    with human interaction with the code.'''

from screen_selector import make_selection # I don't know how much experience you have with linking code from file to file, but here we are just
                                           # taking the function from screen_selector.py and using it with the following environment below.
                                           # This was done for code organizational purposes.

# Create the main Tkinter window that users will a button on.
root = tk.Tk() # The root variable refers to the main window of the application, ex. the window with the botton in it.
root.title("Selection Tool")

# Add the 'make selection' button
screenshot_button = tk.Button(root, text="Make Selection", command=lambda: make_selection(root))
# The lambda function acts as a wrapper for the make_selection function which occurs on button press.

# Alter whitespace padding to ensure button visibility.
screenshot_button.pack(pady=20, padx=20)

# Start the Tkinter event loop. This waits for 'events' (such as mouse clicks or key presses) after which these events can be mapped to functionality.
root.mainloop()