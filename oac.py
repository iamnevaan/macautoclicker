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
waiting_for_hotkey = False

def save_settings():
    """Save hotkey and interval settings."""
    settings = {
        "hotkey": hotkey_char,
        "click_interval": click_interval
    }
    with open(settings_file, "w") as f:
        json.dump(settings, f)

def load_settings():
    """Load settings from file."""
    global hotkey, click_interval, hotkey_char
    try:
        with open(settings_file, "r") as f:
            settings = json.load(f)
            hotkey_char = settings["hotkey"]
            click_interval = float(settings["click_interval"])
            hotkey_label.config(text=f"Hotkey: {hotkey_char}")
            hotkey = KeyCode.from_char(hotkey_char.lower())
            interval_entry.delete(0, tk.END)
            interval_entry.insert(0, str(click_interval))
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

def select_hotkey():
    """Enable hotkey selection mode."""
    global waiting_for_hotkey
    waiting_for_hotkey = True
    hotkey_label.config(text="Press any key...")

def update_hotkey(key):
    """Set the selected key as the hotkey."""
    global hotkey, hotkey_char, waiting_for_hotkey
    if waiting_for_hotkey:
        hotkey_char = key.char if hasattr(key, 'char') and key.char else key.name
        hotkey_label.config(text=f"Hotkey: {hotkey_char.upper()}")
        hotkey = KeyCode.from_char(hotkey_char.lower())
        waiting_for_hotkey = False
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
hotkey_label = tk.Label(root, text="Hotkey: F6")
hotkey_label.grid(row=1, column=0)
hotkey_button = tk.Button(root, text="Set Hotkey", command=select_hotkey)
hotkey_button.grid(row=1, column=1)

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
hotkey_char = "f6"  # Default hotkey character
load_settings()

# Start keyboard listener
listener = Listener(on_press=update_hotkey)
listener.start()

root.mainloop()
