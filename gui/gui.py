import tkinter as tk
from tkinter import ttk


root = tk.Tk()
root.title("Route Advisory Expert System")

tk.Label(root, text="Source Station:").grid(row=0, column=0, padx=10, pady=10)
tk.Label(root, text="Destination Station:").grid(row=1, column=0, padx=10, pady=10)


source_menu = ttk.Combobox(
    root,
    textvariable=source_var,
    values=stations,
    state="readonly"
)
source_menu.grid(row=0, column=1, padx=10, pady=10)

dest_menu = ttk.Combobox(
    root,
    textvariable=dest_var,
    values=stations,
    state="readonly"
)
dest_menu.grid(row=1, column=1, padx=10, pady=10)

output_text = tk.Text(root, height=10, width=50)
output_text.grid(row=3, column=0, columnspan=2, padx=10, pady=10)