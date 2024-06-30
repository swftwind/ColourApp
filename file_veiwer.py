import tkinter as tk
import os
from tkinter import Toplevel, Listbox, Scrollbar, Frame
from tkinter import filedialog
from PIL import Image

# default_folder_path = os.path.expanduser("/screen_selections")
open_windows = {}  # Dictionary to track open windows

def open_selections(root):

    # Check if the selection window is already open (to ensure every file and/or window is only open once).
    if 'selection_window' in open_windows:
        open_windows['selection_window'].lift() # If a window is already open, rather than opening a new one brings it to the top layer.
        return

    folder_path = filedialog.askdirectory() # Opens file browser and asks user to select a directory (which will then be displayed in app)
    if not folder_path:
        return
    
    def open_image(file_path):
        # Same check as above
        if file_path in open_windows:
            open_windows[file_path].lift()
            return

        img_window = Toplevel(root)
        img_window.title(file_path)
        img_label = tk.Label(img_window)
        img_label.pack(pady=10, padx=10)
        img = tk.PhotoImage(file=file_path)
        img_label.config(image=img)
        img_label.image = img

        # Add to open windows dictionary
        open_windows[file_path] = img_window

        def on_close_image_window():
            del open_windows[file_path]
            img_window.destroy()

        img_window.protocol("WM_DELETE_WINDOW", on_close_image_window)

    selection_window = Toplevel(root)
    selection_window.title("Saved Selections")
    selection_window.geometry("600x400")  # Set the default size of the window

    frame = Frame(selection_window)
    frame.pack(fill=tk.BOTH, expand=1)

    scrollbar = Scrollbar(frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    listbox = Listbox(frame, yscrollcommand=scrollbar.set)
    listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
    scrollbar.config(command=listbox.yview)

    for file_name in os.listdir(folder_path):
        if file_name.endswith('.png'):
            listbox.insert(tk.END, file_name)

    def on_double_click(event):
        selected = listbox.get(listbox.curselection())
        file_path = os.path.join(folder_path, selected)
        open_image(file_path)

    listbox.bind("<Double-Button-1>", on_double_click)

    # Add to open windows dictionary
    open_windows['selection_window'] = selection_window

    def on_close_selection_window():
        del open_windows['selection_window']
        selection_window.destroy()

    selection_window.protocol("WM_DELETE_WINDOW", on_close_selection_window)