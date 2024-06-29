import tkinter as tk
from tkinter import messagebox, Toplevel, Canvas
import pyautogui
import datetime
# from PIL import Image

# Function to capture the screenshot of the selected region
def make_selection(root):
    # Minimize the root window
    root.withdraw()
    
    # Create a full-screen transparent window
    top = Toplevel(root) # 'top' is an overlay window created on top 'level' of the existing root window
    top.attributes('-fullscreen', True)
    top.attributes('-alpha', 0.2)
    top.config(bg='black')
    
    # Create a canvas to draw the selection rectangle
    canvas = Canvas(top, cursor="cross", bg='grey', highlightthickness=0) # creates a rectangle in the layer named 'top' that shows
                                                                          # possible selection areas
    canvas.pack(fill=tk.BOTH, expand=tk.YES)
    
    # Variables to store the coordinates of the selected region
    start_x = start_y = curX = curY = 0
    
    def on_mouse_down(event): # saves positions of mouse when it is pressed to compare with endpoints after mouse is dragged.
                              # to determine where the bounds of the rectangular selection are.
        nonlocal start_x, start_y
        start_x = canvas.canvasx(event.x)
        start_y = canvas.canvasy(event.y)
        canvas.create_rectangle(start_x, start_y, start_x, start_y, outline='red', fill='teal', tag="rect")

    def on_mouse_drag(event):
        nonlocal curX, curY
        curX, curY = (event.x, event.y)
        canvas.coords("rect", start_x, start_y, curX, curY)
    
    def on_mouse_up(event):
        nonlocal start_x, start_y, curX, curY
        # Take the screenshot of the selected region
        top.destroy() # Disposes of the top layer as it was just a visual selection guide.
        x = int(min(start_x, curX))
        y = int(min(start_y, curY))
        width = int(abs(start_x - curX))
        height = int(abs(start_y - curY))
        screenshot = pyautogui.screenshot(region=(x, y, width, height)) # pyautogui handles all layering for us to capture anything in top to bottom order
                                                                        # to compile the final selection image

        # Using datetime library to give saved selections timestamped names to ensure filename uniqueness
        current_datetime = datetime.datetime.now()
        timestamp = current_datetime.strftime("%Y-%m-%d_%H-%M-%S") # YY-MM-DD_HH-MM-SS format

        screenshot.save(f"screen_selections/selection_{timestamp}.png") # fstring to use a variable within the filename
        root.deiconify()
        messagebox.showinfo("Colour Tool", f"Selection saved as screenshot_{timestamp}.png.")

    # Bind mouse events to canvas
    canvas.bind("<ButtonPress-1>", on_mouse_down)
    canvas.bind("<B1-Motion>", on_mouse_drag)
    canvas.bind("<ButtonRelease-1>", on_mouse_up)

# MOVED TO MAIN.PY :

# # Create the main Tkinter window
# root = tk.Tk()
# root.title("Snipping Tool")

# # Add the screenshot button
# screenshot_button = tk.Button(root, text="Make Selection", command=make_selection) # changed to lambda function to provide root attribute to this file from main.py
# screenshot_button.pack(pady=20, padx=20)

# # Start the Tkinter event loop
# root.mainloop()