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
        icon_photo = ImageTk.PhotoImage(icon_image) # convert image to a ImageTk photo for display optimization
        img_window.iconphoto(True, icon_photo)

        # Create a frame for the side menu
        menu_frame = Frame(img_window, width=200, height=400, bg='lightgrey')
        menu_frame.pack(side=tk.LEFT, fill=tk.Y)
        menu_frame.pack_propagate(False)

        # Create a nested frame for the buttons
        ui_frame = Frame(menu_frame, bg='lightgrey')
        ui_frame.pack(fill=tk.BOTH, expand=True)
        # Create a frame for the tool buttons
        tool_button_frame = Frame(ui_frame, bg='lightgrey')
        tool_button_frame.pack(anchor='nw', pady=0, padx=0)

        # Load the eyedropper icon
        eyedropper_icon_path = "ui_elements/eyedropper.png"
        eyedropper_icon = Image.open(eyedropper_icon_path)
        eyedropper_icon = eyedropper_icon.resize((40, 40), Image.LANCZOS)
        eyedropper_icon = ImageTk.PhotoImage(eyedropper_icon)

        # Load the eyedropper icon
        zoom_icon_path = "ui_elements/loupe-neutral.png"
        zoom_icon = Image.open(zoom_icon_path)
        zoom_icon = zoom_icon.resize((40, 40), Image.LANCZOS)
        zoom_icon = ImageTk.PhotoImage(zoom_icon)

        def on_eyedropper_selection(img_window):
            if eyedropper_toggle_var.get():
                print("zamn")
                img_window.config(cursor="cross")
                img_label.bind("<Motion>", update_colour_square)  # Bind mouse motion to update colour
                img_label.bind("<Leave>", on_mouse_leave)  # Bind mouse leave to handle out of bounds
            else:
                print("zawg")
                img_window.config(cursor="")
                img_label.unbind("<Motion>")  # Unbind mouse motion
                img_label.unbind("<Leave>")  # Unbind mouse leave

        def on_zoom_selection(img_window):
            if zoom_toggle_var.get():
                print("2zamn")
                img_window.config(cursor="sizing")
                # img_label.bind("<Motion>", update_colour_square)  # Bind mouse motion to update colour
                img_label.bind("<Leave>", on_mouse_leave)  # Bind mouse leave to handle out of bounds
                img_label.bind("<Button-1>", zoom_in)  # Bind left click to zoom-in function
                img_label.bind("<Button-3>", zoom_out)  # Bind right click to zoom-out function
            else:
                print("2zawg")
                img_window.config(cursor="")
                # img_label.unbind("<Motion>")  # Unbind mouse motion
                img_label.unbind("<Leave>")  # Unbind mouse leave
                img_label.unbind("<Button-1>")  # Unbind left click
                img_label.unbind("<Button-3>")  # Unbind right click

        def on_eyedropper_use():
            pass


        def get_pixel_colour(x, y):
            img = Image.open(file_path)
            img = img.convert('RGB')

            if ((x < 0) or (y < 0) or (x >= img.width) or (y >= img.height)):  # Check if coordinates are within bounds
                return None

            pixel_colour = img.getpixel((x, y))
            return f'#{pixel_colour[0]:02x}{pixel_colour[1]:02x}{pixel_colour[2]:02x}'
        
        def update_colour_square(event):
            x = event.x
            y = event.y
            colour = get_pixel_colour(x, y)

            if colour: # if colour has been set to None this will return false.
                colour_square.config(bg=colour)
                label.config(text="", bg=colour)
            # else:
            #     label.config(text="No colour selected.", bg='white')

        def on_mouse_leave(event):
            label.config(text="No colour selected.", bg='white')
            colour_square.config(bg='white')

        
        def zoom_in(event):
            nonlocal current_zoom_level
            current_zoom_level += 0.1
            update_zoom()

        def zoom_out(event):
            nonlocal current_zoom_level
            current_zoom_level -= 0.1
            update_zoom()

        def update_zoom():
            new_width = int(original_img.width * current_zoom_level)
            new_height = int(original_img.height * current_zoom_level)
            img_resized = original_img.resize((new_width, new_height), Image.LANCZOS)
            tk_img_resized = ImageTk.PhotoImage(img_resized)
            img_label.config(image=tk_img_resized)
            img_label.image = tk_img_resized
            return tk_img_resized


        # Create the eyedropper tool button
        eyedropper_toggle_var = tk.IntVar()
        eyedropper_button = ttk.Checkbutton(tool_button_frame, image=eyedropper_icon, variable=eyedropper_toggle_var, style="Toolbutton", command=lambda: on_eyedropper_selection(img_window))
        eyedropper_button.image = eyedropper_icon  # Keep a reference to avoid garbage collection
        eyedropper_button.pack(side='left', pady=10, padx=10)

        # Create the zoom tool button
        zoom_toggle_var = tk.IntVar()
        zoom_button = ttk.Checkbutton(tool_button_frame, image=zoom_icon, variable=zoom_toggle_var, style="Toolbutton", command=lambda: on_zoom_selection(img_window))
        zoom_button.image = zoom_icon  # Keep a reference to avoid garbage collection
        zoom_button.pack(side='right', pady=10, padx=0)

        # Create a square canvas below the eyedropper button
        colour_square = Canvas(ui_frame, width=180, height=180, bg='white', bd=2, highlightbackground='black')
        colour_square.pack(anchor='nw', pady=0, padx=10)
        # Create a label in the middle of the canvas
        label = tk.Label(colour_square, text="No colour selected.", bg='white', fg='grey')
        colour_square.create_window(90, 90, window=label, anchor='center')

        # Load and add the small PNG image to the bottom left of the left UI frame
        logo_path = "ui_elements/branding/Vibrant_Logo_Final_TransparentBG.png"
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
        # Store original image to avoid multiple resizes affecting quality
        original_img = img.copy()
        tk_img = ImageTk.PhotoImage(img)
        # img = img.resize((200, 200), Image.LANCZOS)  # Resize image to desired size
        # Convert the image to a format Tkinter can use
        tk_img = ImageTk.PhotoImage(img)

        # Initialize current zoom level
        current_zoom_level = 1.0

        img_label.config(image=tk_img)
        img_label.image = tk_img

        # Add to open windows dictionary
        open_windows[file_path] = img_window

        def on_close_image_window():
            del open_windows[file_path]
            img_window.destroy()

        img_window.protocol("WM_DELETE_WINDOW", on_close_image_window)

    def open_working_directory():
        working_directory = os.getcwd() + '/screen_selections'  # Get current working directory
        if os.name == 'nt':  # Windows
            os.startfile(working_directory)
        elif os.name == 'posix':  # macOS or Linux
            subprocess.call(['open', working_directory])

    selection_window = Toplevel(root)
    selection_window.title("Saved Selections")
    selection_window.geometry("600x400")  # Set the default size of the window

    # Load and set the custom icon upon creation of the UI window
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

    # Create a frame for the bottom widgets
    bottom_frame = Frame(selection_window)
    bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

    # Add a button to open the working directory
    folder_icon_path = "ui_elements/folder.png"
    folder_icon = Image.open(folder_icon_path)
    folder_icon = folder_icon.resize((30, 30), Image.LANCZOS)
    folder_icon = ImageTk.PhotoImage(folder_icon)

    open_dir_button = tk.Button(bottom_frame, image=folder_icon, command=open_working_directory)
    open_dir_button.image = folder_icon  # Keep a reference to avoid garbage collection
    open_dir_button.pack(side='right', pady=5, padx=5)

    # Load and add the small PNG image to the bottom left of the left UI frame
    logo_path = "ui_elements/branding/Vibrant_Logo_Final_TransparentBG.png"
    logo = Image.open(logo_path)
    logo = logo.resize((100, 40), Image.LANCZOS)  # Resize as needed
    logo = ImageTk.PhotoImage(logo)
    logo_label = tk.Label(bottom_frame, image=logo)
    logo_label.image = logo  # Keep a reference to avoid garbage collection
    logo_label.pack(side='left', pady=2, padx=2)