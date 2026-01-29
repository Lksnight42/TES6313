import tkinter as tk
from tkinter import ttk

from data.map.index import load_locations, NAME_TO_ID, ID_TO_NAME
from gui.handlers import find_route_handler


import loader.loader as loader
from graph.path import explain_top_k


root = tk.Tk()
root.title("Route Advisory Expert System")
root.geometry("900x700")
load_locations()
stations = list(NAME_TO_ID.keys())

source_var = tk.StringVar()
dest_var = tk.StringVar()
preference_var = tk.StringVar(value="cheapest")


tk.Label(root, text="Source Station:").grid(row=0, column=0, padx=10, pady=10)

ttk.Combobox(root, textvariable=source_var, values=stations, state="readonly").grid(row=0, column=1, padx=20, pady=20)

tk.Label(root, text="Destination Station:").grid(row=1, column=0, padx=10, pady=10)

ttk.Combobox(root, textvariable=dest_var, values=stations, state="readonly").grid(row=1, column=1, padx=10, pady=10)

tk.Label(root, text="Preference:").grid(row=2, column=0, padx=180,sticky="w")

pref_frame = tk.Frame(root)
pref_frame.grid(row=2, column=1, padx=10, pady=10, sticky="w")

tk.Radiobutton(
    pref_frame,
    text="Cheapest",
    variable=preference_var,
    value="cheapest"
).pack(side="left", padx=(15, 10))

tk.Radiobutton(
    pref_frame,
    text="Fastest",
    variable=preference_var,
    value="fastest"
).pack(side="left", padx=5)

root.rowconfigure(45, weight=1)
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)

output_text = tk.Text(root, height=30, width=70)
output_text.grid(row=45, column=0, sticky="sw", padx=(10, 0), pady=10)

output_text2 = tk.Text(root, height=30, width=70)
output_text2.grid(row=45, column=1, sticky="se", padx=(0, 10), pady=10)


def on_find_route():
    output_text.delete(1.0, tk.END)
    output_text2.delete(1.0, tk.END)

    src = source_var.get()
    dst = dest_var.get()
    pref = preference_var.get()

    try:
        result = find_route_handler(src,dst,pref)
        render_best_route(result)
        render_top_k_explanations(result["alternatives"])

    except Exception as e:
        output_text.insert(tk.END, f"Error: {e}")

def render_best_route(result):
    best = result["best"]
    s = best["summary"]
    steps = best["steps"]

    def w(text=""):
        output_text.insert(tk.END, text + "\n")

    w("=" * 40)
    w("🚏 Route Recommendation")
    w("=" * 40)

    w(f"From       : {ID_TO_NAME[s['start']]}")
    w(f"To         : {ID_TO_NAME[s['end']]}")
    w(f"Preference : {s['preference'].capitalize()}")
    w("")

    w(f"⏱ Total Time : {s['total_time_min']:.2f} min")
    w(f"💰 Total Cost : RM {s['total_cost_rm']:.2f}")
    w(f"🔁 Transfers  : {s['transfers']}")
    w("")

    w("-" * 40)
    w("🧭 Steps")
    w("-" * 40)

    for i, step in enumerate(steps, 1):
        frm = ID_TO_NAME[step["from"]]
        to = ID_TO_NAME[step["to"]]

        w(f"{i:>2}. {frm} → {to}")
        w(
            f"    🚆 {step['action']} | "
            f"{step['time_min']:.2f} min | "
            f"RM {step['cost_rm']:.2f}"
        )
        w("")

def render_top_k_explanations(explanations):
    def w(text=""):
        output_text2.insert(tk.END, text + "\n")

    w("=" * 40)
    w("📊 Alternative Routes (Top-K)")
    w("=" * 40)

    for exp in explanations:
        w(f"Option #{exp['rank']}")
        for reason in exp["why"]:
            w(f"  • {reason}")
        w("")


tk.Button(root, text="Find Route", command=on_find_route).grid(row=3, column=0, columnspan=2, pady=10)

root.mainloop()
