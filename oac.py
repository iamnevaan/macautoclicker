import time
import threading
import tkinter as tk
import json
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, Key, KeyCode
from PIL import Image, ImageTk
import os

# Initialize mouse controller
mouse = Controller()

# Default settings
settings_file = "clicker_settings.json"
clicking = False
click_interval = 0.01  # Default click speed
hotkey_char = "f6"  # Default hotkey as string
hotkey = KeyCode.from_char(hotkey_char.lower())  # Convert to pynput format
waiting_for_hotkey = False

def save_settings():
    settings = {"hotkey": hotkey_char, "click_interval": click_interval}
    with open(settings_file, "w") as f:
        json.dump(settings, f)

def load_settings():
    global hotkey, click_interval, hotkey_char
    try:
        with open(settings_file, "r") as f:
            settings = json.load(f)
            hotkey_char = settings["hotkey"]
            click_interval = float(settings["click_interval"])
            hotkey_label.config(text=f"Hotkey: {hotkey_char.upper()}")
            hotkey = KeyCode.from_char(hotkey_char.lower())
            interval_entry.delete(0, tk.END)
            interval_entry.insert(0, str(click_interval))
    except (FileNotFoundError, ValueError, KeyError):
        pass

def start_clicking():
    global clicking
    clicking = True
    status_label.config(text="Clicking...", fg="green")
    threading.Thread(target=click_loop, daemon=True).start()

def stop_clicking():
    global clicking
    clicking = False
    status_label.config(text="Stopped.", fg="red")

def click_loop():
    while clicking:
        mouse.click(Button.left)
        time.sleep(click_interval)

def on_press(key):
    global clicking
    if key == hotkey:
        if clicking:
            stop_clicking()
        else:
            start_clicking()

def quit_app():
    stop_clicking()
    root.quit()

def select_hotkey():
    global waiting_for_hotkey
    waiting_for_hotkey = True
    hotkey_label.config(text="Press any key...")

def update_hotkey(key):
    global hotkey, hotkey_char, waiting_for_hotkey
    if isinstance(key, KeyCode):
        hotkey_char = key.char if key.char else key.name
    elif isinstance(key, Key):
        hotkey_char = key.name

    hotkey_label.config(text=f"Hotkey: {hotkey_char.upper()}")
    hotkey = KeyCode.from_char(hotkey_char.lower()) if hotkey_char.isalnum() else key
    waiting_for_hotkey = False
    save_settings()

def update_interval(event):
    global click_interval
    try:
        click_interval = float(interval_entry.get())
        save_settings()
    except ValueError:
        pass

def unified_listener(key):
    global waiting_for_hotkey
    if waiting_for_hotkey:
        update_hotkey(key)
    else:
        on_press(key)

# GUI Setup
root = tk.Tk()
root.title("Auto Clicker")

# Set window icon
file_path = os.path.dirname(os.path.abspath(__file__))
icon_path = os.path.join(file_path, "icon.png")

if os.path.exists(icon_path):
    img = Image.open(icon_path)
    icon = ImageTk.PhotoImage(img)
    root.iconphoto(True, icon)

# Status Label
status_label = tk.Label(root, text="Stopped.", fg="red", font=("Arial", 12, "bold"))
status_label.grid(row=0, column=0, columnspan=2)

# Hotkey selection
hotkey_label = tk.Label(root, text=f"Hotkey: {hotkey_char.upper()}")
hotkey_label.grid(row=1, column=0)
hotkey_button = tk.Button(root, text="Set Hotkey", command=select_hotkey)
hotkey_button.grid(row=1, column=1)

# Click Interval input
tk.Label(root, text="Click Interval (seconds):").grid(row=2, column=0)
interval_entry = tk.Entry(root)
interval_entry.grid(row=2, column=1)
interval_entry.bind("<KeyRelease>", update_interval)

# Buttons
start_button = tk.Button(root, text="Start", command=start_clicking)
start_button.grid(row=3, column=0)

stop_button = tk.Button(root, text="Stop", command=stop_clicking)
stop_button.grid(row=3, column=1)

quit_button = tk.Button(root, text="Quit", command=quit_app)
quit_button.grid(row=4, column=0, columnspan=2)

# Load settings on startup
load_settings()

# Single unified listener
listener = Listener(on_press=unified_listener)
listener.start()

root.mainloop()
