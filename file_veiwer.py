import tkinter as tk
import os
from tkinter import Toplevel, Listbox, Scrollbar, Frame, Canvas
from tkinter import filedialog, ttk
from PIL import Image, ImageTk

# default_folder_path = os.path.expanduser("/screen_selections")
open_windows = {}  # Dictionary to track open windows

def open_selections(root, icon_path):

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

        # Load and set the custom icon
        icon_image = Image.open(icon_path)
        icon_photo = ImageTk.PhotoImage(icon_image)
        img_window.iconphoto(True, icon_photo)

        # Create a frame for the side menu
        menu_frame = Frame(img_window, width=200, height=400, bg='lightgrey')
        menu_frame.pack(side=tk.LEFT, fill=tk.Y)
        menu_frame.pack_propagate(False)

        # Create a nested frame for the button
        button_frame = Frame(menu_frame, bg='lightgrey')
        button_frame.pack(fill=tk.BOTH, expand=True)

        # Load the eyedropper icon
        eyedropper_icon_path = "ui_elements/eyedropper.png"  # Replace with the correct path to the eyedropper icon
        eyedropper_icon = Image.open(eyedropper_icon_path)
        eyedropper_icon = eyedropper_icon.resize((40, 40), Image.LANCZOS)
        eyedropper_icon = ImageTk.PhotoImage(eyedropper_icon)

        def on_eyedropper_selection(img_window):
            if toggle_var.get():
                print("zamn")
                img_window.config(cursor="cross")
            else:
                print("zawg")
                img_window.config(cursor="")

        def on_eyedropper_use():
            pass

        # Create the eyedropper button
        toggle_var = tk.IntVar()
        eyedropper_button = ttk.Checkbutton(button_frame, image=eyedropper_icon, variable=toggle_var, style="Toolbutton", command=lambda: on_eyedropper_selection(img_window))
        eyedropper_button.image = eyedropper_icon  # Keep a reference to avoid garbage collection
        eyedropper_button.pack(anchor='nw', pady=10, padx=10)

        # Create a square canvas below the eyedropper button
        color_square = Canvas(button_frame, width=180, height=180, bg='white', bd=2, highlightbackground='black')
        color_square.pack(anchor='nw', pady=10, padx=10)
        # Create a label in the middle of the canvas
        label = tk.Label(color_square, text="No colour selected.", bg='white', fg='grey')
        color_square.create_window(90, 90, window=label, anchor='center')

        # Load and add the small PNG image to the bottom left of the left UI frame
        logo_path = "ui_elements/branding/Vibrant_Logo_Final_TransparentBG.png"  # Replace with the correct path to your small PNG image
        logo = Image.open(logo_path)
        logo = logo.resize((100, 40), Image.LANCZOS)  # Resize as needed
        logo = ImageTk.PhotoImage(logo)
        logo_label = tk.Label(menu_frame, image=logo, bg='lightgrey')
        logo_label.image = logo  # Keep a reference to avoid garbage collection
        logo_label.pack(side=tk.BOTTOM, anchor='sw', pady=10, padx=10)


        # Create a frame for the image
        img_frame = Frame(img_window)
        img_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)

        img_label = tk.Label(img_window)
        img_label.pack(pady=10, padx=10)
        # Open and (potentially) scale the image using PIL
        img = Image.open(file_path)
        # img = img.resize((200, 200), Image.LANCZOS)  # Resize image to desired size
        # Convert the image to a format Tkinter can use
        tk_img = ImageTk.PhotoImage(img)

        img_label.config(image=tk_img)
        img_label.image = tk_img

        # Add to open windows dictionary
        open_windows[file_path] = img_window

        def on_close_image_window():
            del open_windows[file_path]
            img_window.destroy()

        img_window.protocol("WM_DELETE_WINDOW", on_close_image_window)

    selection_window = Toplevel(root)
    selection_window.title("Saved Selections")
    selection_window.geometry("600x400")  # Set the default size of the window

    # Load and set the custom icon immediately
    icon_image = Image.open(icon_path)
    icon_photo = ImageTk.PhotoImage(icon_image)
    selection_window.iconphoto(True, icon_photo)

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