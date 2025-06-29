import csv
import json
import os
import sys
import uuid
from collections import defaultdict
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import FreeSimpleGUI as sg

# ---------- Utility Functions ----------

def find_columns(header, x_match="time", y_match="force"):
    x_col = y_col = None
    for col in header:
        lc = col.lower()
        if x_col is None and x_match in lc:
            x_col = col
        if y_col is None and y_match in lc:
            y_col = col
    return x_col, y_col

def load_csv_data(filename, x_match="time", y_match="force"):
    with open(filename, newline='') as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames
        x_col, y_col = find_columns(header, x_match, y_match)

        if not x_col or not y_col:
            raise ValueError(f"Could not identify X/Y columns in {filename}.")

        data = defaultdict(list)
        for row in reader:
            try:
                x = float(row[x_col])
                y = float(row[y_col])
                data['x'].append(x)
                data['y'].append(y)
                data['row'].append(row)
            except ValueError:
                continue
    return data, x_col, y_col

def draw_figure(canvas_elem, figure):
    canvas = FigureCanvasTkAgg(figure, canvas_elem.TKCanvas)
    canvas.draw()
    #canvas.get_tk_widget().pack(side='top', fill='both', expand=1)
    canvas.get_tk_widget().grid(row=0, column=0, sticky='nsew')

    return canvas

def save_selected_data(selected_points, all_data, x_col, y_col, raw_filename):
    assessed_data = []
    x_all = all_data['x']
    y_all = all_data['y']
    rows = all_data['row']

    # Closest point selector
    def closest(xc, yc):
        best_idx = None
        best_dist = float("inf")
        for i, (x, y) in enumerate(zip(x_all, y_all)):
            d = (x - xc)**2 + (y - yc)**2
            if d < best_dist:
                best_dist = d
                best_idx = i
        return best_idx

    kept_rows = []
    for (cx, cy) in selected_points:
        idx = closest(cx, cy)
        kept_rows.append(rows[idx])

    assessed_id = str(uuid.uuid4())[:8]
    assessed_filename = f"{os.path.splitext(raw_filename)[0]}__assessed_{assessed_id}.csv"

    with open(assessed_filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(kept_rows)

    return assessed_filename, assessed_id

def update_json_register(json_path, entry):
    if os.path.exists(json_path):
        with open(json_path, 'r') as f:
            register = json.load(f)
    else:
        register = []

    register.append(entry)

    with open(json_path, 'w') as f:
        json.dump(register, f, indent=2)

# ---------- Main App ----------

def launch_assessment(csv_filename, x_col_includ="time", y_col_includ="force"):
    data, x_col, y_col = load_csv_data(csv_filename, x_col_includ, y_col_includ)

    fig, ax = plt.subplots()
    ax.plot(data['x'], data['y'], label="Raw Data")
    ax.set_title(f"{x_col} vs {y_col}")
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    ax.grid(True)

    crosshair, = ax.plot([], [], 'ro', label='Selected', markersize=8)
    selected = []

    sg.theme("LightGrey1")
    #layout = [
    #    [sg.Canvas(key='-CANVAS-')],
    #    [sg.Button("Save & Close"), sg.Button("Cancel")]
    #]
    layout = [
    [sg.Canvas(key='-CANVAS-', size=(640, 480), expand_x=True, expand_y=True)],
    [sg.Button("Save & Close"), sg.Button("Cancel")]
    ]


    window = sg.Window("Data Assessor", layout, finalize=True)
    canvas = draw_figure(window['-CANVAS-'], fig)
    window['-CANVAS-'].expand(True, True)


    def onclick(event):
        if event.xdata is None or event.ydata is None:
            return
        x, y = event.xdata, event.ydata
        selected.append((x, y))
        xs, ys = zip(*selected)
        crosshair.set_data(xs, ys)
        fig.canvas.draw()

    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    

    while True:
        event, _ = window.read()
        if event in (sg.WIN_CLOSED, "Cancel"):
            break
        elif event == "Save & Close":
            assessed_file, assess_id = save_selected_data(
                selected, data, x_col, y_col, os.path.basename(csv_filename)
            )

            # Update JSON register
            register_entry = {
                "assessment_id": assess_id,
                "raw_filename": csv_filename,
                "assessed_filename": assessed_file,
                "x_col": x_col,
                "y_col": y_col
            }
            update_json_register("assessments_register.json", register_entry)
            break

    window.close()


# ---------- Entry Point ----------

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="Path to CSV file")
    parser.add_argument("--xcol", help="Partial match for X column", default="time")
    parser.add_argument("--ycol", help="Partial match for Y column", default="force")
    args = parser.parse_args()

    launch_assessment(args.filename, args.xcol, args.ycol)
