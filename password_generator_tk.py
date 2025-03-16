import tkinter as tk
from tkinter import filedialog, scrolledtext
import subprocess
import os
import configparser

# Function to read config file
def read_config():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "config.ini")
    config = configparser.ConfigParser()
    config.read(config_path)
    return config

# Load configuration
config = read_config()
script_path = config.get("Settings", "script_path")
wlfDir = config.get("Settings", "wordlist_folder")

# Custom window without default title bar
def move_window(event):
    root.geometry(f"+{event.x_root}+{event.y_root}")

def close_app():
    root.destroy()


def select_file():
    filename = filedialog.askopenfilename(filetypes=[("Text files", "wordlist_*.txt"), ("All files", "*.*")],initialdir=wlfDir)
    if filename:
        file_entry.delete(0, tk.END)
        file_entry.insert(0, filename)

def run_script():
    filepath = file_entry.get()
    if filepath:
        try:
            # Set the script name
            script_name = script_path + "\password_generator_list.py"
            result = subprocess.run(["python", script_name, filepath], capture_output=True, text=True)
            output_text.delete(1.0, tk.END)
            output_text.insert(tk.END, result.stdout)
            if result.stderr:
                output_text.insert(tk.END, "\nERROR:\n" + result.stderr)
        except Exception as e:
            output_text.insert(tk.END, f"\nERROR: {str(e)}")



root = tk.Tk()
root.overrideredirect(True)  # Remove default title bar
root.geometry("950x680")  # Set initial window size
root.configure(bg="#d0d0d0")  # Set background color of the main window

# Custom title bar
bg_color = "#18057a"
title_bar = tk.Frame(root, bg=bg_color, relief="raised", bd=2)
title_bar.pack(fill=tk.X)
title_label = tk.Label(title_bar, text="Password Generator", bg=bg_color, fg="white", font=("Bahnschrift", 12))
title_label.pack(side=tk.LEFT, padx=10)
title_bar.bind("<B1-Motion>", move_window)
title_label.bind("<B1-Motion>", move_window)
close_button = tk.Button(title_bar, text="X", command=close_app, bg=bg_color, fg="white", borderwidth=0)
close_button.pack(side=tk.RIGHT, padx=5)

frame = tk.Frame(root, bg="#d0d0d0")
frame.pack(padx=10, pady=10)

file_entry = tk.Entry(frame, width=50, bg="#ffffff", fg="#000000")
file_entry.grid(row=0, column=0, padx=5, pady=5)

browse_button = tk.Button(frame, text="Select Wordlist file", command=select_file, bg="#007BFF", fg="white")
browse_button.grid(row=0, column=1, padx=5, pady=5)

ok_button = tk.Button(frame, text="Generate passwords", command=run_script, bg="#28A745", fg="white")
ok_button.grid(row=0, column=10, padx=5, pady=5)

cancel_button = tk.Button(frame, text="Exit", command=close_app, bg="#DC3545", fg="white")
cancel_button.grid(row=0, column=20, padx=5, pady=5)

output_text = scrolledtext.ScrolledText(root, width=130, height=35, bg="#ffffff", fg="#000000")
output_text.pack(padx=10, pady=10)

root.mainloop()