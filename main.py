# initial commit for main.py

# test
# test 2

print("zamn zawg")


import tkinter as tk
# The following imports below are used to display icons in taskbar and on window panels.
import pystray
from PIL import Image as PILImage
import threading
import ctypes  # Required for setting the app icon in the taskbar on Windows

''' TKInter is a standard inferface and gui library that we will be using to create windows, buttons, dipsplay photos, and mostly anything related
    to human interaction with the code.'''

import os
from screen_selector import make_selection # I don't know how much experience you have with linking code from file to file, but here we are just
                                           # taking the function from screen_selector.py and using it with the following environment below.
                                           # This was done for code organizational purposes.
from file_veiwer import open_selections

# Create the main Tkinter window that users will a button on.
root = tk.Tk() # The root variable refers to the main window of the application, ex. the window with the botton in it.
root.title("Vibrant")
root.geometry("300x100")

# Load and set the custom icon for the main window and taskbar
icon_path = "ui_elements/branding/Vibrant_Icon_Final_TransparentBG.ico"

# Create a function to set the taskbar icon
def create_tray_icon():
    icon_image = PILImage.open(icon_path)
    menu = pystray.Menu(pystray.MenuItem('Exit', lambda: root.quit()))
    icon = pystray.Icon("name", icon_image, "Vibrant", menu)
    icon.run()

# Run the system tray icon in a separate thread
tray_icon_thread = threading.Thread(target=create_tray_icon, daemon=True)
tray_icon_thread.start()

# Ensure the icon is also used for the taskbar
if os.name == 'nt':  # This only works on Windows
    app_id = 'vibrant.1.0'  # Arbitrary string that acts as the unique process identifier.
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
    root.iconbitmap(icon_path)
else:
    root.iconbitmap(icon_path) # In case OS is not Windows, this command on its own should be sufficient.


# Variable for (constant) button width
button_width = 15

# Add the 'make selection' button
new_selection_button = tk.Button(root, text="Make Selection", width=button_width, command=lambda: make_selection(root, icon_path))
# The lambda function acts as a wrapper for the make_selection function which occurs on button press.

# Alter whitespace padding to ensure button visibility.
new_selection_button.pack(anchor='nw', pady=10, padx=10)

# Add the 'open selections' button
open_selections_button = tk.Button(root, text="Open Selections", width=button_width, command=lambda: open_selections(root, icon_path))
# This button will open a file dialog to select a directory and display saved selections.
# It also uses a lambda function as tk root object data needs to be handed to file_veiwer.py to allow
# drawing and access to the common canvases created by this file.

# Alter whitespace padding to ensure button visibility.
open_selections_button.pack(anchor='nw', pady=0, padx=10)

# Start the Tkinter event loop. This waits for 'events' (such as mouse clicks or key presses) after which these events can be mapped to functionality.
root.mainloop()