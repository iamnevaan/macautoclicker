import time
import threading
import tkinter as tk
import json
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode
from PIL import Image, ImageTk
import os

# Initialize mouse controller
mouse = Controller()

# Default settings
settings_file = "clicker_settings.json"
clicking = False
start_key = KeyCode(char='s')
stop_key = KeyCode(char='q')
click_interval = 0.01

# Function to save settings
def save_settings():
    settings = {
        "start_key": start_entry.get(),
        "stop_key": stop_entry.get(),
        "click_interval": interval_entry.get()
    }
    with open(settings_file, "w") as f:
        json.dump(settings, f)

# Function to load settings
def load_settings():
    global start_key, stop_key, click_interval
    try:
        with open(settings_file, "r") as f:
            settings = json.load(f)
            start_entry.delete(0, tk.END)
            start_entry.insert(0, settings["start_key"])
            stop_entry.delete(0, tk.END)
            stop_entry.insert(0, settings["stop_key"])
            interval_entry.delete(0, tk.END)
            interval_entry.insert(0, settings["click_interval"])
            start_key = KeyCode(char=settings["start_key"])
            stop_key = KeyCode(char=settings["stop_key"])
            click_interval = float(settings["click_interval"])
    except (FileNotFoundError, ValueError, KeyError):
        pass

# Function to start clicking
def start_clicking():
    global clicking
    clicking = True
    threading.Thread(target=click_loop, daemon=True).start()

# Function to stop clicking
def stop_clicking():
    global clicking
    clicking = False

# Function to handle the clicking loop
def click_loop():
    while clicking:
        mouse.click(Button.left)
        time.sleep(click_interval)

# Function to set hotkeys
def set_hotkeys():
    global start_key, stop_key
    start_key = KeyCode(char=start_entry.get())
    stop_key = KeyCode(char=stop_entry.get())
    save_settings()

# Function to set the interval
def set_interval():
    global click_interval
    try:
        click_interval = float(interval_entry.get())
        save_settings()
    except ValueError:
        pass  # Optionally show an error message here

# Function to handle key press events
def on_press(key):
    if key == start_key:
        start_clicking()
    elif key == stop_key:
        stop_clicking()

# Function to quit the application
def quit_app():
    stop_clicking()
    root.quit()

# GUI Setup
root = tk.Tk()

# Get the file path to the icon
file_path = os.path.dirname(os.path.abspath(__file__))
icon_path = os.path.join(file_path, "icon.png")

# Open the image using PIL
img = Image.open(icon_path)

# Convert the image to PhotoImage
icon = ImageTk.PhotoImage(img)

# Set the icon for the window
root.iconphoto(True, icon)

# Set window title
root.title("Auto Clicker")

# GUI elements
tk.Label(root, text="Start Hotkey:").grid(row=0, column=0)
start_entry = tk.Entry(root)
start_entry.grid(row=0, column=1)

tk.Label(root, text="Stop Hotkey:").grid(row=1, column=0)
stop_entry = tk.Entry(root)
stop_entry.grid(row=1, column=1)

tk.Label(root, text="Click Interval (seconds):").grid(row=2, column=0)
interval_entry = tk.Entry(root)
interval_entry.grid(row=2, column=1)

set_hotkeys_button = tk.Button(root, text="Set Hotkeys", command=set_hotkeys)
set_hotkeys_button.grid(row=3, column=0, columnspan=2)

set_interval_button = tk.Button(root, text="Set Interval", command=set_interval)
set_interval_button.grid(row=4, column=0, columnspan=2)

start_button = tk.Button(root, text="Start", command=start_clicking)
start_button.grid(row=5, column=0)

stop_button = tk.Button(root, text="Stop", command=stop_clicking)
stop_button.grid(row=5, column=1)

quit_button = tk.Button(root, text="Quit", command=quit_app)
quit_button.grid(row=6, column=0, columnspan=2)

load_settings()  # Load settings on startup

# Start listener for keyboard hotkeys
listener = Listener(on_press=on_press)
listener.start()

root.mainloop()
