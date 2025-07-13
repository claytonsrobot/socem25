import FreeSimpleGUI as sg
import serial
import serial.tools.list_ports
import threading
import csv
import json
import time
from datetime import datetime
import logging
logger = logging.getLogger(__name__)

from src.socem25.decoractors import log_function_call

# Globals
collecting = False
serial_thread = None
CONFIG_FILE = 'config.json'

# Load serial config or use default
@log_function_call(level=logging.INFO)
def load_config():
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {'port': 'COM3', 'baudrate': 9600}

@log_function_call(level=logging.INFO)
def save_config():
    with open(CONFIG_FILE, 'w') as f:
        json.dump(serial_config, f, indent=4)

serial_config = load_config()

@log_function_call(level=logging.INFO)
def generate_identifier():
    return 'test_' + datetime.now().strftime('%Y%m%d_%H%M%S')

@log_function_call(level=logging.INFO)
def read_serial_data(csv_filename):
    global collecting
    start_time = time.time()

    try:
        with serial.Serial(serial_config['port'], serial_config['baudrate'], timeout=1) as ser, \
             open(csv_filename, 'w', newline='') as csvfile:

            print(f"Opened file: {csv_filename}")
            writer = csv.writer(csvfile)
            writer.writerow(['elapsed_time_sec', 'force', 'displacement'])

            while collecting:
                line = ser.readline().decode(errors='ignore').strip()
                print("Line read:", line)
                if not line:
                    continue
                try:
                    force, displacement = map(float, line.split(','))
                    elapsed_time = time.time() - start_time
                    writer.writerow([elapsed_time, force, displacement])
                    csvfile.flush()
                    print("Parsed and wrote:", elapsed_time, force, displacement)
                except Exception as e:
                    print(f"Data parse error: {e}")
    except Exception as e:
        sg.popup_error(f"Error opening serial port: {e}")


@log_function_call(level=logging.INFO)
def save_metadata(values, test_identifier, unix_timestamp):
    metadata = {
        'test_identifier': test_identifier,
        'entity_id': values['-ENTITY-'],
        'group': values['-GROUP-'],
        'sub_group': values['-SUBGROUP-'],
        'timestamp': datetime.now().isoformat(),
        'csv_file': f"{unix_timestamp}_data.csv",
        'metadata_file': f"{unix_timestamp}_metadata.json",
        'serial_config': serial_config.copy()
    }

    with open(metadata['metadata_file'], 'w') as f:
        json.dump(metadata, f, indent=4)

    try:
        with open('master_test_log.json', 'r') as f:
            master_log = json.load(f)
    except FileNotFoundError:
        master_log = {}

    master_log[str(unix_timestamp)] = metadata

    with open('master_test_log.json', 'w') as f:
        json.dump(master_log, f, indent=4)

@log_function_call(level=logging.INFO)
def start_collection(values):
    global collecting, serial_thread
    collecting = True

    test_identifier = generate_identifier()
    unix_timestamp = int(time.time())
    csv_filename = f"{unix_timestamp}_data.csv"

    serial_thread = threading.Thread(
        target=read_serial_data, args=(csv_filename,), daemon=True
    )
    serial_thread.start()

    save_metadata(values, test_identifier, unix_timestamp)
    return test_identifier

@log_function_call(level=logging.INFO)
def stop_collection():
    global collecting
    collecting = False

@log_function_call(level=logging.INFO)
def open_serial_settings_window():
    layout = [
        [sg.Text('Serial Port:'), sg.Input(serial_config['port'], key='-SET_PORT-')],
        [sg.Text('Baud Rate:'), sg.Input(str(serial_config['baudrate']), key='-SET_BAUD-')],
        [sg.Button('Save'), sg.Button('Cancel')]
    ]
    win = sg.Window('Serial Settings', layout, modal=True)
    while True:
        event, values = win.read()
        if event in (sg.WIN_CLOSED, 'Cancel'):
            break
        elif event == 'Save':
            serial_config['port'] = values['-SET_PORT-']
            try:
                serial_config['baudrate'] = int(values['-SET_BAUD-'])
                save_config()
            except ValueError:
                sg.popup_error("Baud rate must be an integer.")
                continue
            break
    win.close()

@log_function_call(level=logging.INFO)
def auto_detect_serial_port():
    ports = serial.tools.list_ports.comports()
    available = [p.device for p in ports]
    if available:
        serial_config['port'] = available[0]
        save_config()
        sg.popup(f"Auto-detected port: {available[0]}")
    else:
        sg.popup_error("No serial ports found.")

# GUI Layout
menu = [['Settings', ['Serial Config', 'Find Port']]]

layout = [
    [sg.Menu(menu)],
    [sg.Text('Entity Unique ID:'), sg.Input('', key='-ENTITY-')],
    [sg.Text('Group:'), sg.Input('', key='-GROUP-')],
    [sg.Text('Sub-group:'), sg.Input('', key='-SUBGROUP-')],
    [sg.Button('Start Test'), sg.Button('Stop Test'), sg.Button('Exit')]
]

window = sg.Window('Serial Data Collector', layout)

# Event loop
while True:
    event, values = window.read(timeout=100)
    if event in (sg.WINDOW_CLOSED, 'Exit'):
        stop_collection()
        break
    elif event == 'Start Test':
        if values['-ENTITY-']:
            start_collection(values)
        else:
            sg.popup_error("Please provide at least an Entity Unique ID.")
    elif event == 'Stop Test':
        stop_collection()
        sg.popup("Test stopped and data saved.")
    elif event == 'Serial Config':
        open_serial_settings_window()
    elif event == 'Find Port':
        auto_detect_serial_port()

window.close()
