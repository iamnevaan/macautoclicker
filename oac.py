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
click_interval = 0.01  # Default click speed
hotkey = KeyCode.from_char('f6')  # Default hotkey

def save_settings():
    """Save hotkey and interval settings."""
    settings = {
        "hotkey": hotkey_entry.get(),
        "click_interval": interval_entry.get()
    }
    with open(settings_file, "w") as f:
        json.dump(settings, f)

def load_settings():
    """Load settings from file."""
    global hotkey, click_interval
    try:
        with open(settings_file, "r") as f:
            settings = json.load(f)
            hotkey_entry.delete(0, tk.END)
            hotkey_entry.insert(0, settings["hotkey"])
            interval_entry.delete(0, tk.END)
            interval_entry.insert(0, settings["click_interval"])
            hotkey = KeyCode.from_char(settings["hotkey"].lower())
            click_interval = float(settings["click_interval"])
    except (FileNotFoundError, ValueError, KeyError):
        pass

def start_clicking():
    """Start auto-clicking in a separate thread."""
    global clicking
    clicking = True
    status_label.config(text="Clicking...", fg="green")
    threading.Thread(target=click_loop, daemon=True).start()

def stop_clicking():
    """Stop auto-clicking."""
    global clicking
    clicking = False
    status_label.config(text="Stopped.", fg="red")

def click_loop():
    """Click repeatedly while clicking is True."""
    while clicking:
        mouse.click(Button.left)
        time.sleep(click_interval)

def on_press(key):
    """Handle key presses to start/stop clicking."""
    if key == hotkey:
        if clicking:
            stop_clicking()
        else:
            start_clicking()

def quit_app():
    """Stop clicking and quit the app."""
    stop_clicking()
    root.quit()

def update_hotkey(event):
    """Update hotkey entry when a key is pressed."""
    global hotkey
    key = event.keysym
    hotkey_entry.delete(0, tk.END)
    hotkey_entry.insert(0, key.upper())
    hotkey = KeyCode.from_char(key.lower())  # Update hotkey
    save_settings()

def update_interval(event):
    """Update click interval when input changes."""
    global click_interval
    try:
        click_interval = float(interval_entry.get())
        save_settings()
    except ValueError:
        pass  # Ignore invalid input

# GUI Setup
root = tk.Tk()
root.title("Auto Clicker")

# Get the file path to the icon
file_path = os.path.dirname(os.path.abspath(__file__))
icon_path = os.path.join(file_path, "icon.png")

# Open the image using PIL
img = Image.open(icon_path)

# Convert the image to PhotoImage
icon = ImageTk.PhotoImage(img)

# Set the icon for the window
root.iconphoto(True, icon)

# Status Label
status_label = tk.Label(root, text="Stopped.", fg="red", font=("Arial", 12, "bold"))
status_label.grid(row=0, column=0, columnspan=2)

# Hotkey selection
tk.Label(root, text="Hotkey:").grid(row=1, column=0)
hotkey_entry = tk.Entry(root, width=10)
hotkey_entry.grid(row=1, column=1)
hotkey_entry.bind("<KeyPress>", update_hotkey)  # Auto-update hotkey

# Click Interval input
tk.Label(root, text="Click Interval (seconds):").grid(row=2, column=0)
interval_entry = tk.Entry(root)
interval_entry.grid(row=2, column=1)
interval_entry.bind("<KeyRelease>", update_interval)  # Auto-update interval

# Buttons
start_button = tk.Button(root, text="Start", command=start_clicking)
start_button.grid(row=3, column=0)

stop_button = tk.Button(root, text="Stop", command=stop_clicking)
stop_button.grid(row=3, column=1)

quit_button = tk.Button(root, text="Quit", command=quit_app)
quit_button.grid(row=4, column=0, columnspan=2)

# Load settings on startup
load_settings()

# Start keyboard listener
listener = Listener(on_press=on_press)
listener.start()

root.mainloop()
