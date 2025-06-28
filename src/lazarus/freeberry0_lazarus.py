#!/usr/bin/python3
"""
StemBerry V.14 - FreeSimpleGUI Refactor
Description: SOCEM code for system control (commands & communicates w/ main Arduino), GUI, & data storage
Refactored from tkinter to FreeSimpleGUI
Original Developer: Austin Bebee
Edited by: Clayton Bennett
Refactored for FreeSimpleGUI: Assistant

Contents (in order):
- Libraries
- Global Variables
- Utility Classes
- GUI Application Class
- Main execution
"""

from pathlib import Path
import serial
import serial.tools.list_ports
import time
import platform
import threading
import xlsxwriter
import matplotlib
from matplotlib import style
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import subprocess
import sys
import os
import numpy as np
import peakutils
import math
import struct
import PIL.ImageTk
import PIL.Image

# FreeSimpleGUI import
import FreeSimpleGUI as sg

# Try to import lazarus modules (may need path adjustment)
try:
    import lazarus.EI_Interaction_Fx as EI_Interaction_Fx
    import lazarus.EI_No_Interaction_Fx as EI_No_Interaction_Fx
except ImportError:
    print("Warning: lazarus modules not found, EI calculations disabled")
    EI_Interaction_Fx = None
    EI_No_Interaction_Fx = None

# Configuration
generate_rich_files_toggle = True
address = Path(__file__).resolve().parent

# Data storage lists
elapsed = ['Time (s)']
dis = ['Distance (in.)']
force = ['Force (lbs.)']
rowForce = list()
rowMax = list()
rowAve = list()
cropHeight = list()
rowNum = list()
stemNum = list()
countDis = list()

meanF = list()
greatMean = list()
medianF = list()
medianPos = list()
maxF = list()
avelocity = list()
hz = list()
sampling = list()
aveCount = list()
density = list()
spacing = list()
FbHeight = list()

# Auto Force/row peaks
Peaks = list()
avePeak = list()

# Auto EI estimations
EII = list()
EIN = list()
EIave = list()

# Error tracking
errors = list()
errorCodes = list()

# Matplotlib graph settings
style.use("ggplot")
f = Figure(figsize=(4.85, 3.9), dpi=75)
a = f.add_subplot(111)
a.set_ylim(0, 25)

# Conversion Factors
convert = 2.20462262  # kg to lbs
inchonvert = (((math.pi * (0.764)) * 31.4136) / 359)  # converts displacement to inches
vis = "s"  # set to live graph for data display


class Utilities:
    @staticmethod
    def serial_connect(verbose=True):
        """Establish a serial connection to an Arduino or other device."""
        try:
            ports = list(serial.tools.list_ports.comports())
            if not ports:
                raise IOError("No serial ports found.")

            for port in ports:
                try:
                    if verbose:
                        print(f"[INFO] Trying port: {port.device}")
                    ser = serial.Serial(port=port.device, baudrate=115200, timeout=0.5)
                    if verbose:
                        print(f"[SUCCESS] Connected to {port.device}")
                    return ser
                except (serial.SerialException, OSError) as e:
                    if verbose:
                        print(f"[WARN] {port.device} unavailable: {e}")
            raise IOError("No available serial ports.")
            
        except Exception as e:
            if verbose:
                print(f"[ERROR] Serial connection failed: {e}")
            return None

    @staticmethod
    def serial_re_connect(ser):
        """Reconnect serial if disconnected."""
        if ser and ser.is_open:
            ser.close()
        ser = Utilities.serial_connect(verbose=True)
        if ser:
            print("Ready to communicate!")
            sg.popup("Serial Reconnected", "Successfully reconnected to device!")
        else:
            print("Connection failed.")
            sg.popup_error("Connection Failed", "Could not reconnect to serial device.")
        return ser

    @staticmethod
    def keyboard_onscreen():
        """Launch virtual keyboard based on OS."""
        system = platform.system()
        try:
            if system == "Windows":
                subprocess.Popen(["start", "osk"], shell=True)
            elif system == "Linux":
                subprocess.Popen(["florence"])
            elif system == "Darwin":
                print("macOS virtual keyboard not implemented.")
            else:
                print(f"No virtual keyboard support for OS: {system}")
        except Exception as e:
            print(f"[ERROR] Failed to launch virtual keyboard: {e}")

    @staticmethod
    def data_display(visual):
        """Change display method."""
        global vis
        vis = visual
        return vis


class StemBerryGUI:
    def __init__(self):
        self.ser = None
        self.collect = False
        self.current_window = None
        self.data_thread = None
        
        # Set theme
        sg.theme('LightBlue3')
        
        # Initialize serial connection
        self.connect_serial()
        
    def connect_serial(self):
        """Initialize serial connection."""
        self.ser = Utilities.serial_connect(verbose=True)
        if not self.ser:
            sg.popup_error("Serial Connection Failed", 
                          "Could not connect to Arduino.\nPlease check connection and try again.")

    def create_menu_bar(self):
        """Create menu bar for the application."""
        return [
            ['File', ['Serial Reconnect', 'Errors', '---', 'Exit']],
            ['Data Display', ['Data Scrollbars', 'None']],
            ['Help', ['Guide', 'About']]
        ]

    def create_home_layout(self):
        """Create the home/geometry input screen layout."""
        layout = [
            [sg.Menu(self.create_menu_bar())],
            [sg.Text('INPUTS', font=('Arial', 17, 'bold'), justification='center', expand_x=True)],
            [sg.Text('(complete before collecting data)', font=('Arial', 14, 'bold'), 
                    justification='center', expand_x=True)],
            [sg.HSeparator()],
            
            # Stem Count Section
            [sg.Frame('Stem Count Data', [
                [sg.Text('Left Row Stem Count:', font=('Arial', 14, 'bold')), 
                 sg.Input('100', key='-LEFT_ROW_COUNT-', size=(6, 1)),
                 sg.Text('Right Row Stem Count:', font=('Arial', 14, 'bold')), 
                 sg.Input('106', key='-RIGHT_ROW_COUNT-', size=(6, 1))],
                [sg.Text('Horizontal Range of Stem Counts (in.):', font=('Arial', 14, 'bold'))],
                [sg.Input('60', key='-START_COUNT-', size=(6, 1)), 
                 sg.Text('to'), 
                 sg.Input('100', key='-END_COUNT-', size=(6, 1))],
                [sg.Text('Avg. Stem Count:', font=('Arial', 14, 'italic')), 
                 sg.Input('103', key='-AVG_STEM_COUNT-', size=(8, 1), disabled=True),
                 sg.Text('per (in.):', font=('Arial', 14, 'italic')), 
                 sg.Input('40', key='-PER_DIS-', size=(6, 1), disabled=True)]
            ])],
            
            # Force Bar and Stem Height Section
            [sg.Frame('Measurement Parameters', [
                [sg.Text('Forcebar Height (in.):', font=('Arial', 14, 'bold')), 
                 sg.Input('7.5', key='-FB_HEIGHT-', size=(8, 1)),
                 sg.Text('(measured from the middle of the forcebar)', font=('Arial', 12, 'italic'))],
                [sg.Text('Avg. Stem Height (in.):', font=('Arial', 14, 'bold')), 
                 sg.Input('10', key='-STEM_HEIGHT-', size=(8, 1))],
                [sg.Text('# of Contact Rows:', font=('Arial', 14, 'bold')), 
                 sg.Input('4', key='-CONTACT_ROWS-', size=(6, 1)),
                 sg.Text('(likely will stay the same for all plots in a field)', font=('Arial', 12, 'italic'))]
            ])],
            
            # SOCEM Travel Direction Section
            [sg.Frame('SOCEM Travel Direction', [
                [sg.Text('* relative to the front of the plot', font=('Arial', 12, 'italic'))],
                [sg.Radio('Forward', 'DIRECTION', key='-DIR_FORWARD-', default=True, font=('Arial', 12, 'bold')),
                 sg.Radio('Reverse', 'DIRECTION', key='-DIR_REVERSE-', font=('Arial', 12, 'bold'))],
                [sg.Radio('Left to Right', 'DIRECTION', key='-DIR_LEFT_RIGHT-', font=('Arial', 12, 'bold')),
                 sg.Radio('Right to Left', 'DIRECTION', key='-DIR_RIGHT_LEFT-', font=('Arial', 12, 'bold'))]
            ])],
            
            [sg.VPush()],
            
            # Navigation Buttons
            [sg.Column([
                [sg.Button('Collect\nData', size=(10, 3), font=('Arial', 16, 'bold'),
                          button_color=('white', 'darkgray'))],
                [sg.Button('Calibrate\nForce\nSensor', size=(10, 3), font=('Arial', 16, 'bold'),
                          button_color=('white', 'darkgray'))],
                [sg.Button('Keyboard', size=(10, 3), font=('Arial', 16, 'bold'),
                          button_color=('white', 'darkgray'))]
            ], element_justification='center', vertical_alignment='top'),
             sg.Push(),
             sg.Button('Guide', size=(10, 3), font=('Arial', 16, 'bold'),
                      button_color=('white', 'darkgray'))],
            
            # Status Bar
            [sg.StatusBar(f'Serial: {"Connected" if self.ser else "Disconnected"}',
                         size=(50, 1), key='-STATUS-')]
        ]

    def create_data_collection_layout(self):
        """Create the data collection screen layout."""
        layout = [
            [sg.Menu(self.create_menu_bar())],
            [sg.Text('Data Collection', font=('Arial', 18, 'bold'))],
            [sg.HSeparator()],
            
            # Control Panel
            [sg.Frame('Collection Controls', [
                [sg.Button('Start Collection', key='-START_COLLECT-', size=(15, 2),
                          button_color=('white', 'green')),
                 sg.Button('Stop Collection', key='-STOP_COLLECT-', size=(15, 2),
                          button_color=('white', 'red'), disabled=True),
                 sg.Button('Save Data', key='-SAVE_DATA-', size=(15, 2)),
                 sg.Button('Clear Data', key='-CLEAR_DATA-', size=(15, 2))],
                [sg.Text('Sample Rate (Hz):'), sg.Input('10', key='-SAMPLE_RATE-', size=(8, 1)),
                 sg.Text('Collection Time (s):'), sg.Input('60', key='-COLLECT_TIME-', size=(8, 1))]
            ])],
            
            # Data Display
            [sg.Frame('Live Data', [
                [sg.Column([
                    [sg.Text('Force (lbs):', font=('Arial', 12, 'bold'))],
                    [sg.Text('0.00', key='-FORCE_VAL-', font=('Arial', 14), size=(10, 1))],
                    [sg.Text('Distance (in):', font=('Arial', 12, 'bold'))],
                    [sg.Text('0.00', key='-DISTANCE_VAL-', font=('Arial', 14), size=(10, 1))],
                    [sg.Text('Time (s):', font=('Arial', 12, 'bold'))],
                    [sg.Text('0.00', key='-TIME_VAL-', font=('Arial', 14), size=(10, 1))]
                ], vertical_alignment='top'),
                 sg.VSeparator(),
                 sg.Column([
                    [sg.Text('Data Points Collected:')],
                    [sg.Text('0', key='-DATA_COUNT-', font=('Arial', 14))],
                    [sg.Text('Max Force:')],
                    [sg.Text('0.00', key='-MAX_FORCE-', font=('Arial', 14))],
                    [sg.Text('Average Force:')],
                    [sg.Text('0.00', key='-AVG_FORCE-', font=('Arial', 14))]
                 ], vertical_alignment='top')]
            ])],
            
            # Graph placeholder (would need matplotlib integration)
            [sg.Frame('Force vs Distance Graph', [
                [sg.Text('Graph would be displayed here', justification='center', 
                        size=(50, 10), relief=sg.RELIEF_SUNKEN)]
            ])],
            
            # Navigation
            [sg.Button('Back to Home', size=(15, 2)),
             sg.Push(),
             sg.Button('Generate Report', size=(15, 2))]
        ]
        return layout

    def create_calibration_layout(self):
        """Create the load cell calibration screen layout."""
        layout = [
            [sg.Menu(self.create_menu_bar())],
            [sg.Text('Load Cell Calibration', font=('Arial', 18, 'bold'))],
            [sg.HSeparator()],
            
            [sg.Frame('Calibration Instructions', [
                [sg.Text('1. Remove all weights from the load cell')],
                [sg.Text('2. Click "Zero Load Cell" to set zero point')],
                [sg.Text('3. Place known weight on load cell')],
                [sg.Text('4. Enter weight value and click "Calibrate"')],
                [sg.Text('5. Test calibration with known weights')]
            ])],
            
            [sg.Frame('Calibration Controls', [
                [sg.Button('Zero Load Cell', size=(15, 2), button_color=('white', 'blue')),
                 sg.Text('Known Weight (lbs):'), 
                 sg.Input(key='-CAL_WEIGHT-', size=(10, 1)),
                 sg.Button('Calibrate', size=(15, 2), button_color=('white', 'orange'))],
                [sg.Text('Current Reading:'), 
                 sg.Text('0.00 lbs', key='-CAL_READING-', font=('Arial', 12, 'bold'))],
                [sg.Text('Calibration Factor:'),
                 sg.Text('1.000', key='-CAL_FACTOR-', font=('Arial', 12, 'bold'))]
            ])],
            
            [sg.Frame('Test Calibration', [
                [sg.Text('Place test weight and verify reading:')],
                [sg.Text('Expected:', size=(10, 1)), sg.Input(key='-TEST_EXPECTED-', size=(10, 1)),
                 sg.Text('Actual:', size=(10, 1)), sg.Text('0.00', key='-TEST_ACTUAL-', size=(10, 1))],
                [sg.Button('Test Reading', size=(15, 2))]
            ])],
            
            [sg.Button('Back to Home', size=(15, 2)),
             sg.Push(),
             sg.Button('Save Calibration', size=(15, 2), button_color=('white', 'green'))]
        ]
        return layout

    def create_error_report_layout(self):
        """Create the error report screen layout."""
        layout = [
            [sg.Menu(self.create_menu_bar())],
            [sg.Text('Error Report', font=('Arial', 18, 'bold'))],
            [sg.HSeparator()],
            
            [sg.Frame('Recent Errors', [
                [sg.Listbox(values=[], size=(60, 10), key='-ERROR_LIST-')],
                [sg.Button('Clear Errors', size=(15, 2)),
                 sg.Button('Export Error Log', size=(15, 2))]
            ])],
            
            [sg.Frame('System Status', [
                [sg.Text('Serial Connection:'), 
                 sg.Text('Connected' if self.ser else 'Disconnected', 
                        key='-SERIAL_STATUS-')],
                [sg.Text('Last Error:'), 
                 sg.Text('None', key='-LAST_ERROR-')],
                [sg.Text('Error Count:'), 
                 sg.Text('0', key='-ERROR_COUNT-')]
            ])],
            
            [sg.Button('Back to Home', size=(15, 2)),
             sg.Push(),
             sg.Button('Test Systems', size=(15, 2))]
        ]
        return layout

    def run_home_window(self):
        """Run the home window."""
        layout = self.create_home_layout()
        window = sg.Window('StemBerry Control System', layout, 
                          size=(800, 600), finalize=True)
        
        while True:
            event, values = window.read()
            
            if event == sg.WIN_CLOSED or event == 'Exit':
                break
            elif event == 'Start Data Collection':
                window.close()
                self.run_data_collection_window()
                break
            elif event == 'Calibrate Load Cell':
                window.close()
                self.run_calibration_window()
                break
            elif event == 'View Guide':
                sg.popup('Guide', 'User guide would be displayed here.')
            elif event == 'Serial Reconnect':
                self.ser = Utilities.serial_re_connect(self.ser)
                window['-STATUS-'].update(f'Serial: {"Connected" if self.ser else "Disconnected"}')
            elif event == 'Errors':
                window.close()
                self.run_error_report_window()
                break
        
        window.close()

    def run_data_collection_window(self):
        """Run the data collection window."""
        layout = self.create_data_collection_layout()
        window = sg.Window('Data Collection', layout, 
                          size=(900, 700), finalize=True)
        
        while True:
            event, values = window.read(timeout=100)
            
            if event == sg.WIN_CLOSED or event == 'Exit':
                break
            elif event == 'Back to Home':
                window.close()
                self.run_home_window()
                break
            elif event == '-START_COLLECT-':
                self.collect = True
                window['-START_COLLECT-'].update(disabled=True)
                window['-STOP_COLLECT-'].update(disabled=False)
                # Start data collection thread here
            elif event == '-STOP_COLLECT-':
                self.collect = False
                window['-START_COLLECT-'].update(disabled=False)
                window['-STOP_COLLECT-'].update(disabled=True)
            elif event == '-SAVE_DATA-':
                # Implement data saving
                sg.popup('Save Data', 'Data saving functionality would be implemented here.')
            elif event == '-CLEAR_DATA-':
                # Implement data clearing
                sg.popup('Clear Data', 'Data cleared successfully.')
        
        window.close()

    def run_calibration_window(self):
        """Run the calibration window."""
        layout = self.create_calibration_layout()
        window = sg.Window('Load Cell Calibration', layout,
                          size=(800, 600), finalize=True)
        
        while True:
            event, values = window.read()
            
            if event == sg.WIN_CLOSED or event == 'Exit':
                break
            elif event == 'Back to Home':
                window.close()
                self.run_home_window()
                break
            elif event == 'Zero Load Cell':
                # Implement zero calibration
                sg.popup('Zero Calibration', 'Load cell zeroed successfully.')
            elif event == 'Calibrate':
                # Implement calibration with known weight
                weight = values['-CAL_WEIGHT-']
                sg.popup('Calibration', f'Calibrated with {weight} lbs.')
        
        window.close()

    def run_error_report_window(self):
        global errors, errorCodes
        """Run the error report window."""
        layout = self.create_error_report_layout()
        window = sg.Window('Error Report', layout,
                          size=(700, 500), finalize=True)
        
        # Update error list
        window['-ERROR_LIST-'].update(errors if errors else ['No errors recorded'])
        
        while True:
            event, values = window.read()
            
            if event == sg.WIN_CLOSED or event == 'Exit':
                break
            elif event == 'Back to Home':
                window.close()
                self.run_home_window()
                break
            elif event == 'Clear Errors':
                #global errors, errorCodes
                errors.clear()
                errorCodes.clear()
                window['-ERROR_LIST-'].update(['No errors recorded'])
                sg.popup('Errors Cleared', 'All errors have been cleared.')
        
        window.close()

    def run(self):
        """Main application entry point."""
        try:
            self.run_home_window()
        except Exception as e:
            sg.popup_error('Application Error', f'An error occurred: {str(e)}')
        finally:
            if self.ser and self.ser.is_open:
                self.ser.close()


def main():
    """Main function to run the application."""
    app = StemBerryGUI()
    app.run()


if __name__ == "__main__":
    main()