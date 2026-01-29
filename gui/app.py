import tkinter as tk
from tkinter import ttk

from data.map.index import load_locations, NAME_TO_ID, ID_TO_NAME, VALID_LOCATION_IDS
from gui.handlers import find_route_handler


import loader.loader as loader
from graph.path import print_user_route_result


root = tk.Tk()
root.title("Route Advisory Expert System")
root.geometry("900x700")
load_locations()
stations = list(NAME_TO_ID.keys())

source_var = tk.StringVar()
dest_var = tk.StringVar()

tk.Label(root, text="Source Station:").grid(row=0, column=0, padx=10, pady=10)
tk.Label(root, text="Destination Station:").grid(row=1, column=0, padx=10, pady=10)

ttk.Combobox(root, textvariable=source_var, values=stations, state="readonly").grid(row=0, column=1, padx=20, pady=20)

ttk.Combobox(root, textvariable=dest_var, values=stations, state="readonly").grid(row=1, column=1, padx=10, pady=10)

output_text = tk.Text(root, height=30, width=100)
output_text.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

def on_find_route():
    output_text.delete(1.0, tk.END)

    src = source_var.get()
    dst = dest_var.get()

    try:
        result = find_route_handler(src,dst)
        render_result(result)
    except Exception as e:
        output_text.insert(tk.END, f"Error: {e}")

def render_result(result):
    s = result["summary"]

    output_text.insert(
        tk.END,
        f"Route from {ID_TO_NAME[s['start']]}"
        f"to {ID_TO_NAME[s['end']]}\n\n"
    )

    output_text.insert(
        tk.END,
        f"Total time: {s['total_time_min']:.2f} minutes\n"
        f"Total cost: RM {s['total_cost_rm']:.2f}\n"
        f"Transfer : {s['transfers']}\n\n"
    )

    output_text.insert(tk.END, "Steps:\n")

    for i, step in enumerate(result["steps"], 1):
        frm = ID_TO_NAME[step["from"]]
        to = ID_TO_NAME[step["to"]]

        output_text.insert(
            tk.END,
            f"{i}. {frm} -> {to} \n"
            f"   {step['action']} |"
            f"{step['time_min']:.2f} min |"
            f"RM {step['cost_rm']:.2f}\n\n"
        )


tk.Button(root, text="Find Route", command=on_find_route).grid(row=2, column=0, columnspan=2, pady=10)

root.mainloop()