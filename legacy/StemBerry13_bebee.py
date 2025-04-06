#!/usr/bin/python3
#do not erase (needed to be executable for autostart)

'''
StemBerry V.13 
Description: SOCEM code for system control (commands & communicates w/ main Arduino), GUI, & data storage
Last updated: 3/13/2022
Developer: Austin Bebee
Edited by: Clayton Bennett

Contents (in order):
- Libraries
- Global Variables
- Global Functions
- GUI Class
    - Home / geo. input screen
    - Data collection screen
        - Runs data collection function
        - Stores data & saves data
        - Runs automatic stats & saves data
        - Plots F v D graph
    - Load cell calibration screen
    - Error report screen
- Excute GUI command


Fix:
- Appended data issue when writing xlsx files, which comes from ".insert(" command.
- Remove forcebar correction based on wooden ruler, which has not been used as a reference in 2020 or 2021.
'''
generate_rich_files_toggle = 0 # set to no, because I don't use em anyways
#Data File Saving Locations:
#Make sure this is USB address for saving data to
usb = '/media/pi/0000-0001' # update code so data is saved here too
#RPi backup saving location:
address = '/home/pi/Desktop/SAVED_DATA_2020'
address = r'C:\Users\clayton\OneDrive - University of Idaho\AqMEQ\SOCEM\SOCEM_DATA_2020_troubleshoot'
path = address
#address = '/home/pi/Desktop/SAVED DATA 2019/RAW_'

#Needed libraries
#from serial import Serial
import serial.tools.list_ports
import time
import tkinter as tk
#from tkinter import 
import threading
import xlsxwriter
import csv
import matplotlib
from matplotlib import style
matplotlib.use("TkAgg")
#from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
#import matplotlib.animation as animation
import matplotlib.pyplot as plt
#import itertools
import subprocess
import sys
import os
from os import path
import numpy as np
import EI_Interaction_Fx # script that computes EI assuming full interactions
import EI_No_Interaction_Fx # script that computes EI assuming no interactions
import optiH # script that determine optiaml force bar height
import peakutils
#from PeakUtils.Plot import plot as pplot
import math
import struct
import PIL.ImageTk
import PIL.Image

#Global varibles  
collect = False # controls data collection loop from GUI frontend
getCount = False
clearDisplay = True




# old way
decoded_bytes = list() # 
string = list()
dis = list()
force = list()
rowForce = list()
rowMax = list()
rowAve = list()
cropHeight = list()
elapsed = list()
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
aveHeight = list()
aveCount = list()
density = list()
spacing = list()
FbHeight = list()

# new way, to get rid of style: elapsed.insert(0 , "Time (s)")
decoded_bytes = list() # 
string = list()
elapsed = ['Time (s)']
dis = ['Distance (in.)']
force = ['Force (lbs.)']
rowForce = list()
rowMax = list()
rowAve = list()
cropHeight = list() #['Height (in.)']
rowNum = list() #['Rows']
stemNum = list() #['Ave Stem Count']
countDis = list() #['Sample Distance (in.)']

meanF = list()
greatMean = list()
medianF = list()
medianPos = list()
maxF = list()
avelocity = list()
hz = list()
sampling = list()
aveHeight = list()
aveCount = list()
density = list()
spacing = list()
FbHeight = list() #['Fb Bottom Height (in.)']

# auto Force/row peaks
Peaks = list()
avePeak = list()

# auto EI estimations
EII = list()
EIN = list()
EIave = list()

# for tracking errors
errors = list()
errorCodes = list()

#matplotlib graph settings
style.use("ggplot")
f = Figure(figsize=(4.85,3.9), dpi=75)
a = f.add_subplot(111)
a.set_ylim(0, 25)

#Conversion Factors
convert = 2.20462262 #kg to lbs
#inchonvert = (((.764/1.70)*31.125)/359) #converts to inches traveled, wheel dia. = 31.125
inchonvert = (((math.pi*(0.764))*31.4136)/359) # converts displacement to inches, wheel diameter = 31.4136
vis = "s" #set to live graph for data display

# Determine Arduino serial port address
def SerConnect():


    try:
        ports = serial.tools.list_ports.comports()
        #print(ports)
        #dev = '/dev/ttyACM0'
        dev = ports[0].device
        dev = 'COM3'
        ser = serial.Serial(dev, 115200)
        #print(ports)
        #print(dev)
        #dev = 'COM13'

##        ser = serial.Serial(
##        port = "/dev/ttyUSB2",
##        baudrate = 115200,
##        bytesize = serial.EIGHTBITS, 
##        parity = serial.PARITY_NONE,
##        stopbits = serial.STOPBITS_ONE, 
##        timeout = 1,
##        xonxoff = False,
##        rtscts = False,
##        dsrdtr = False,
##        writeTimeout = 2
##        )

        #ser.open()
        #ser.isOpen()
    except:
        # FIX THIS, WE NEVER get ERROR e1 CB 4/5/2022
        error = 'serial connection'
        eCode = 'e1'
        errors.append(error) # append error label
        errorCodes.append(eCode) # append error code
        popup('serial connection')

    return ser
    

# if serial disconnect (unplugged) reconnect - NOTE: doesn't properly work currently. 
def SerReconnect(ser): 
    ser.close()
    SerConnect()

#virtual keyboard
def keyboard():
    key = subprocess.Popen(['florence'], stdout=subprocess.PIPE, shell = False)

#changes display method    #DELETE?
def data_display(visual):
    global vis
    vis = visual
    return vis

#if any error occurs, display popup error msg
def popup(error):
    popup = tk.Tk()
    popup.wm_title("Error")
    Elabel = tk.Label(popup, text="A {} error occurred.".format(error), font=("arial", 12, "bold"))
    Elabel.pack(side="top", fill="x", pady=10)               
    popup.mainloop()

def showErrors(self):
    self.show_frame(ErrorReport) # show Error Report page
    ErrorReport.showErrors2(self.frames[ErrorReport]) # display errors in lists 
    
#if filename already exists - prompt user to rename
def rename(name):
    popup = tk.Tk()
    popup.wm_title('Filename already exists.')
    renameIt = tk.Label(popup, text = '"{}" already exists in the saving location. Please rename and press Save.'.format(name), font = ('arial', 12, 'bold'))
    renameIt.pack(side='top', fill='x', pady=10)
    popup.mainloop()

#closes GUI (from file menubar)
def close():
    python = sys.executable
    os.execl(python, python, * sys.argv)

# * # DATA COLLECTION FUNCTION - Acquires live data from Arduino # * #
def run(self, ser):
    try:        
        started = 's'
        ser.write(started.encode()) #sends 's' to arduino, telling it to start
        #print('s')
    except:
        errors.append('serial com. (start data)') # label 
        eCode = 'e2'
        errorCodes.append(eCode)
        popup('start data collect')

    #DATA COLLECTION CODE

    elapsed = ['Time (s)']
    dis = ['Distance (in.)']
    force = ['Force (lbs.)']

    if vis == 's':# data displayed in scrollbars (default)
        # Displays incoming data 
        scroll = tk.Scrollbar(self)

        self.timeLabel = tk.Label(self, text = "s",font = ("arial", 14, "bold"), fg = "dodgerblue2", bg = "ghost white")
        self.timeLabel.place(x = 274, y = 70)
        self.Timelist = tk.Listbox(self, yscrollcommand = scroll.set, bg = "ghost white",highlightbackground = "gray2", width = 7, height = 1, font = ("arial", 14, "bold"), fg = "dodgerblue2")
        self.Timelist.place(x = 240, y = 100)

        self.disLabel = tk.Label(self, text = "in.",font = ("arial", 14, "bold"), fg = "dodgerblue2", bg = "ghost white")
        self.disLabel.place(x = 357, y = 70)
        self.Dislist = tk.Listbox(self, yscrollcommand = scroll.set, bg = "ghost white",highlightbackground = "gray2", width = 7, height = 1, font = ("arial", 14, "bold"), fg = "dodgerblue2")
        self.Dislist.place(x = 330, y = 100)

        self.forceLabel = tk.Label(self, text = "lbs.",font = ("arial", 14, "bold"), fg = "dodgerblue2", bg = "ghost white")
        self.forceLabel.place(x = 444, y = 70)
        self.Forcelist = tk.Listbox(self, yscrollcommand = scroll.set, bg = "ghost white",highlightbackground = "gray2", width = 7, height = 11, font = ("arial", 14, "bold"), fg = "dodgerblue2")
        self.Forcelist.place(x = 420, y = 100)

    else:# user decided for no data display
        try:#clear scrollbars if they were there
            self.Dislist.place_forget()
            self.Forcelist.place_forget()
            self.Timelist.place_forget()
            self.disLabel.place_forget()
            self.forceLabel.place_forget()
            self.timeLabel.place_forget()
        except:# no scrollbars
            pass
    
    i = 0
    

    try:
    
        while collect == True: # GUI in fSerConnect()rontend controls value of collect to start/stop loop
            
            if ser.inWaiting() > 0: #checks to see if Serial is available 
            
                try: #make sure serial data can be read/is there
                    ser_bytes = ser.readline()
                except:
                    errors.append('serial read') # label 
                    eCode = 'e3'
                    errorCodes.append(eCode)
                    popup("serial read")
        

                if i == 0:
                    start = time.time() #stopwatch starts

                #DELETE?
                #decoded_bytes.insert(i,(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))) # acquires & decodes bytes (incoming Arduino data)
                #string.insert(i,str(decoded_bytes[i])) # inserts decoded bytes into string

                bytesDecoded = (ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
                string.insert(i,str(bytesDecoded)) # inserts decoded bytes into string
                #print(' run ser read ', string[i]) # useful debugging tool
                split = string[i].split("|") # splits data at | (1st = distance, 2nd = force)
                   
                if len(split) >= 2 and split[0] != "" and split[1] != "": #makes sure data is in proper formatting before processing (else pair: A)
                    inches = split[0]
                    pounds = split[1]
                    
                    try:
                        # insert changed to extend, CB, HERE
                        elapsed.extend(time.time() - start)# list of elapsed time
                        dis.extend(float(inches))# list of inches traveled 
                        force.extend(float(pounds))# list of force traveled

##                        elapsed.insert(i, time.time() - start)# list of elapsed time
##                        dis.insert(i, float(inches))# list of inches traveled 
##                        force.insert(i, float(pounds))# list of force traveled

                    except:
                        errors.append('data append') # label 
                        eCode = 'e4'
                        errorCodes.append(eCode)  
                     #   popup("Arduino data error")
                      #  print(string[i])

                    '''Scrollbars Options'''
                    # if scrollbars option = on:
                    try: # puts data on GUI display by default (user can turn off)  
                        self.Dislist.insert(END, str(dis[i]))# inserts at end of listbox to actually display
                        self.Dislist.see(END)# makes sure listbox is at end so it displays live data
                        self.Forcelist.insert(END, str('%.2f' % force[i]))
                        self.Forcelist.see(END)
                        self.Timelist.insert(END, str('%.2f' % elapsed[i]))
                        self.Timelist.see(END)

                    #scrollbars options = off        
                    except:
                        pass
                    
                    i = i+1
                              
                else: # skips incoming data if not in right format (if pair: A
                    errors.append('data skip (incorrect format)') # label 
                    eCode = 'e5'
                    errorCodes.append(eCode)                    
    except:
        if collect == True:
            errors.append('serial disconnect')
            eCode = 'e6'
            errorCodes.append(eCode)
        else:
            pass

# GUI overarching class
class GUI(tk.Tk):
    def __init__(self, *args, **kwargs):# automatically runs
        
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side='top', fill='both',expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # top menu configuration
        menubar = tk.Menu(container)
        datamenu = tk.Menu(menubar, tearoff=0)
        #datamenu.add_command(label="Live Graph", command = lambda:data_display("g"))
        datamenu.add_command(label="Data Scrollbars", command = lambda:data_display("s"))
        datamenu.add_command(label="None", command = lambda:data_display(""))
        filemenu = tk.Menu(menubar, tearoff=0)
        #filemenu.add_command(label='Errors', command = lambda:self.show_frame(ErrorReport))#, showErrors(self))
        filemenu.add_command(label='Serial Reconnect', command = lambda:SerReconnect(ser))
        filemenu.add_command(label='Errors', command = lambda:showErrors(self))
        filemenu.add_command(label="Exit", command = lambda:close())
        menubar.add_cascade(label='File', menu=filemenu)
        menubar.add_cascade(label="Data Display", menu=datamenu)
        
        tk.Tk.config(self, menu=menubar)                
        self.frames = {}# empty dictionary

        for F in (Home, DataCollect, Calibrate, Guide, ErrorReport, Heights):# must put all pages in here
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')
            frame.configure(background = 'ghost white')
            
        self.show_frame(Home)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

        frame.event_generate("<<ShowFrame>>") # event


##class UploadPage(tk.Frame):
##    def __init__(self, parent, controller):
##        ...
##        self.bind("<<ShowFrame>>", self.on_show_frame)
##
##    def on_show_frame(self, event):
##        print("I am being shown...")

#Home page 
class Home(tk.Frame):
    
    def __init__(self, parent, controller): # automatically runs
        # global variables within Home that are used in multiple Classes & functions
        global ser # serial port
        global barHeight # tracks force bar height
        global rows # tracks # of rows inSerConnect() contact w/ force bar
        global stemCount # tracks ave stem count
        global perDis # tracks stem count distance
        global stemHeight # tracks ave stem height
        global rowCountLeft, rowCountRight # tracks manual counts
        global startCount, endCount # tracks horizontal range of manual counts
        global Fb_bottom, Fb_center, Fb_place
        global usePlotnameAsFilenameYN, plotText
        
        tk.Frame.__init__(self, parent)
        
        # GUI design (text, user inputs (text input, buttons):
        homeheader = tk.Label(self, text = "INPUTS",
                          font = ("arial", 17, "bold"), fg = "gray3", bg="ghost white").place(x=350,y=0)
        first = tk.Label(self, text = "(complete before collecting data)",
                          font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white").place(x=245,y=30)

        # y = 255, 220, 285, 80, 150, 185, 115
        '''
        plotText = tk.StringVar()
        plotText.set("")
        plotLabel = tk.Label(self, text = "Plot: ",
                          font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white").place(x=0,y=80)
        plotEntry = tk.Entry(self, textvariable=plotText,
                font = ("arial", 14, "bold"), width= 10, bg="white", fg="gray1").place(x = 75, y = 80)
        plotPostLabel = tk.Label(self, text = "(Example: 'HW429')",
                          font = ("arial", 14, "italic"), fg = "gray3", bg="ghost white").place(x=200,y=80)
        
        ''
        usePlotnameAsFilenameYN = tk.IntVar()
        usePlotnameAsFilenameYN.set(1)
        #plotnameAsfilenameLabel = tk.Label(self, text = "Use Plot Name as File Name?",
        #                  font = ("arial", 10, ""), fg = "gray3", bg="ghost white").place(x=230,y=80)
        plotnameAsFilenameCheckbox = tk.Checkbutton(self, text= "Use Plot Name as File Name?",variable = usePlotnameAsFilenameYN).grid(row=0, sticky=W)
        '''

        rowCountLeft = tk.IntVar()
        rowCountRight = tk.IntVar()
        rowCountLeft.set(100)
        rowCountRight.set(106)
        rowCountLeftLabel = tk.Label(self, text = "Left Row Stem Count:",
                          font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white").place(x=0,y=120)
        rowCountRightLabel = tk.Label(self, text = "Right Row Stem Count:",
                          font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white").place(x=300,y=120)
        rowCountLeftEntry = tk.Entry(self, textvariable=rowCountLeft,
                font = ("arial", 14, "bold"), width= 4, bg="white", fg="gray1").place(x = 220, y = 120)
        rowCountRightEntry = tk.Entry(self, textvariable=rowCountRight,
                font = ("arial", 14, "bold"), width= 4, bg="white", fg="gray1").place(x = 540, y = 120)
        
        startCount = tk.IntVar()
        endCount = tk.IntVar()
        startCount.set(60)
        endCount.set(100)
        startCountDisLabel = tk.Label(self, text = "Horizontal Range of Stem Counts (in.):",
                          font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white").place(x=0,y=160)
        endCountDisLabel = tk.Label(self, text = " to ",
                          font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white").place(x=415,y=160)
        startCountEntry = tk.Entry(self, textvariable=startCount,
                font = ("arial", 14, "bold"), width= 4, bg="white", fg="gray1").place(x = 365, y = 160)
        endCountEntry = tk.Entry(self, textvariable=endCount,
                font = ("arial", 14, "bold"), width= 4, bg="white", fg="gray1").place(x = 455, y = 160)

        
        barHeight = tk.DoubleVar() # Whatever number is typed into the field
        Fb_place = 7.5 # default value, which can be altered 
        barHeight.set(Fb_place) #
        Fb_center = barHeight # CB 3/13/2022 # In 2021 the ruler was not used, and the ruler is risky.
        Fb_bottom = Fb_center.get() - .32
        barHeightLabel = tk.Label(self, text = "Forcebar Height (in.):",
                          font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white").place(x=0,y=200) 
        barHeightEntry = tk.Entry(self, textvariable=barHeight,
               font = ("arial", 14, "bold"), width= 6, bg="white", fg="gray1").place(x = 200, y = 200)
        barHeightPostLabel = tk.Label(self, text = "(measured from the middle of the forcebar)",
                          font = ("arial", 14, "italic"), fg = "gray3", bg="ghost white").place(x=290,y=200)
        
        stemHeightLabel = tk.Label(self, text = "Avg. Stem Height (in.):",
                          font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white").place(x=0,y=240)
        stemHeight = tk.DoubleVar()
        stemHeight.set(10)# sets initial stem height to 10 (ave. estimate observed)
        stemHeightEntry = tk.Entry(self, textvariable=stemHeight,
                font = ("arial", 14, "bold"), width= 6, bg="white", fg="gray1").place(x = 210, y = 240)

        rows = tk.IntVar()
        rows.set(4)#sets rows to be 4 initially since typical number
        rowsLabel = tk.Label(self, text = "# of Contact Rows:",
                font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white").place(x=0,y=280)
        rowsEntry = tk.Entry(self, textvariable=rows,
               font = ("arial", 14, "bold"), width= 4, bg="white", fg="gray1").place(x = 190, y = 280)
        rowsPostLabel = tk.Label(self, text = "(likely will stay the same for all plots in a field)",
                font = ("arial", 14, "italic"), fg = "gray3", bg="ghost white").place(x=250,y=280)
        
        # possibly get rid of this box, though the variable needs to be kept for passing to storage
        stemCount = tk.DoubleVar()
        stemCount.set(99)
        stemCount.set((rowCountLeft.get()+rowCountRight.get())/2)
        stemCountLabel = tk.Label(self, text = "Avg. Stem Count:",
                          font = ("arial", 14, "italic"), fg = "gray3", bg="ghost white").place(x=0,y=320)
        stemCountEntry = tk.Entry(self, textvariable=stemCount,
                font = ("arial", 14, "italic"), width= 6, bg="white", fg="gray1").place(x = 161, y = 320)
        
        # possibly get rid of this box, though the variable needs to be kept for passing to storage
        perDisLabel = tk.Label(self, text = "per (in.):",
                          font = ("arial", 14, "italic"), fg = "gray3", bg="ghost white").place(x=240,y=320)
        perDis = tk.IntVar()# counting stem distance
        perDis.set(44)# standard distance used (approx. 1 meter)
        perDis.set(endCount.get()-startCount.get())
        perDisEntry = tk.Entry(self, textvariable=perDis,
                font = ("arial", 14, "italic"), width= 6, bg="white", fg="gray1").place(x = 320, y = 320)

        self.directionChoice = tk.IntVar()
        self.directionChoice.set(1)
        frameRadioDirection = tk.LabelFrame(self, text='SOCEM Travel Direction*',font = ("arial", 12, "bold"), width= 6, bg="white", fg="gray1")
        frameRadioDirection.place(x = 410, y = 320)

        reverse = tk.Radiobutton(frameRadioDirection, text='Reverse', variable=self.directionChoice, value=4,font = ("arial", 12, "bold")).grid(row=0, columnspan=3)
        leftToRight = tk.Radiobutton(frameRadioDirection, text='Left to Right', variable=self.directionChoice, value=3,font = ("arial", 12, "bold")).grid(row=1, column=1)
        rightToLeft = tk.Radiobutton(frameRadioDirection, text="Right to Left", variable=self.directionChoice, value=2,font = ("arial", 12, "bold")).grid(row=1, column=2)
        forward = tk.Radiobutton(frameRadioDirection, text="Forward", variable=self.directionChoice, value=1,font = ("arial", 12, "bold")).grid(row=2, columnspan=3)
        print("var = ", self.directionChoice.get())
        

        frameRadioDirectionPostLabel = tk.Label(self, text = "* relative to the front of the plot",
                font = ("arial", 12, "italic"), fg = "gray3", bg="ghost white").place(x=440,y=440)
        
        # button that enters DataCollect page/class
        dataB = tk.Button(self, text = "Collect\nData",
                       font = ("arial", 16, "bold"), height = 3, width = 8, fg = "ghost white", bg = "gray2",
                       command=lambda:controller.show_frame(DataCollect)).place(x = 675, y = 40)
        # button that enters Calibrate page/class
        calibrateB = tk.Button(self, text = "Calibrate\nForce\nSensor",
                       font = ("arial", 16, "bold"), height = 3, width = 8, fg = "ghost white", bg = "gray2",
                       command=lambda:controller.show_frame(Calibrate)).place(x = 675, y = 224)
        #tares/zeros load cell
        guideB = tk.Button(self, text = "Guide", font = ("arial", 16, "bold"), height = 3, width = 8, fg = "ghost white", bg = "gray2",command=lambda:controller.show_frame(Guide))
        guideB.place(x = 0, y = 360)

        heightsB = tk.Button(self, text = "Heights", font = ("arial", 16, "bold"), height = 3, width = 8, fg = "ghost white", bg = "gray2",command=lambda:controller.show_frame(Heights))
        heightsB.place(x = 675, y = 40+92)

        keyB = tk.Button(self, text = "Keyboard",
                       font = ("arial", 16, "bold"), height = 3, width = 8, fg = "ghost white", bg = "gray2",
                       command=keyboard).place(x = 675, y = 316)
        print("in")
        ser = SerConnect()
        #SerReconnect(ser)

        print("")
        self.bind("<<ShowFrame>>", self.on_show_frame_Inputs)

        #return usePlotnameAsFilenameYN, plotText
    
    def on_show_frame_Inputs(self, event):
        print("Return to Input screen, text fields updated")
        stemCount.set((rowCountLeft.get()+rowCountRight.get())/2)
        perDis.set(endCount.get()-startCount.get())
        Fb_center = barHeight # CB 3/13/2022 # In 2021 the ruler was not used, and the ruler is risky.
        Fb_bottom = Fb_center.get() - .32
        try: # this doesn't work if you're going from the Collect Data page to the Input page
            stemHeight.set(aveH)# the issue, is aveH doesn't exist yet pulls in calculated value from Heights page
            barHeight.set(Fb_place) # pulls in calculated value from Heights page
        except:
            print("Height calculator not used.")
        

# Data collection page
class DataCollect(tk.Frame):
    
    
    #window = Tk()
    #filename = tk.StringVar()
    def __init__(self, parent, controller):# automatically runs

        
        # global filename
        
        
        self.dataset = 1 # tracks dataset number 
        self.pastSet = self.dataset
        self.legends = []
        #self.legends = list()
        
        tk.Frame.__init__(self, parent)

        #GUI design of this page
        label = tk.Label(self, text ="DATA COLLECTION",
                         font = ("arial", 17, "bold"), fg = "gray3", bg="ghost white").place(x=275,y=0)

        #button that goes back to 1st page (Inputs / home)
        HomeB = tk.Button(self, text ="Inputs",
                        font = ("arial", 16, "bold"), height = 3, width = 8, fg = "ghost white", bg = "gray2",
                        command=lambda:controller.show_frame(Home)).place(x = 0, y = 316)
        
        keyB = tk.Button(self, text = "Keyboard",
               font = ("arial", 16, "bold"), height = 3, width = 8, fg = "ghost white", bg = "gray2",
               command=keyboard).place(x = 675, y = 316)
        
        name = tk.Label(self, text = "Filename: ",
                         font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white").place(x=0,y=35)
        
        #self.filename = filename.get()
        self.filename = tk.StringVar()# user inputted filename
        '''
        if usePlotnameAsFilenameYN.get() == 1:
            print('Top')
            self.filename = tk.StringVar() 
            #self.filename = plotText # this does work, but the objects are married
            self.filename.set(plotText.get()) # this doesn't work, but at least the object isn't married
        elif usePlotnameAsFilenameYN.get() == 0:
            self.filename = tk.StringVar()# user input filename

        filenameEntry = tk.Entry(self, textvariable=self.filename,
                          font = ("arial", 14, "bold"), width="32", bg="white", fg="gray1")
        filenameEntry.place(x = 96, y = 35)
        '''
        
        self.entry_box = tk.Entry(self, textvariable=self.filename,
                          font = ("arial", 14, "bold"), width="32", bg="white", fg="gray1")
        self.entry_box.place(x = 96, y = 35)
        ''
        #gives access to buttons for data collection control 
        newB = tk.Button(self, text = "New",
                        font = ("arial", 16, "bold"), height = 3, width = 8, fg = "ghost white", bg = "gray2",command=lambda:self.named(self.filename)).place(x = 550, y = 40)

        #plotnameB = tk.Button(self, text = "Use Plotname as Filename",
         #               font = ("arial", 16, "bold"), height = 2, width = 12, fg = "ghost white", bg = "gray2",command=lambda:self.plotnameToFilename(plotname.get())).place(x = 0, y = 220)

        self.bind("<<ShowFrame>>", self.on_show_frame_DataCollection)
        
    def on_show_frame_DataCollection(self, event):
        # global filename # putting this here fixed it
        
        print("Flip to Date Collect screen, text fields updated")
        stemCount.set((rowCountLeft.get()+rowCountRight.get())/2)
        perDis.set(endCount.get()-startCount.get())
        Fb_center = barHeight # CB 3/13/2022 # In 2021 the ruler was not used, and the ruler is risky.
        Fb_bottom = Fb_center.get() - .32
        '''
        if usePlotnameAsFilenameYN.get()==1:
            print("Bottom")
            #self.filename = plotText  # this does work, but the objects are married
            self.filename = tk.StringVar()
            self.filename.set(plotText.get()) # this doesn't work, but at least the object isn't married
            print(self.filename.get())
        elif usePlotnameAsFilenameYN.get()==0:
            print(self.filename.get())
            #self.filename = tk.StringVar()

        #return filename
        '''
            

    #def plotnameToFilename (self, plotname)
        
    
    def named(self, filename):
        global clearDisplay # used to indicate whether or not to clear data display

        if self.dataset == 1: #set initial previous filename
            self.prevName = filename.get()
        
        currentName = filename.get() #gets current name
        newOne = self.dataset - self.pastSet #checks to see if a new dataset is being made after 'New' button is pressed

        if currentName != self.prevName:# check if inputted filename has changed 
            self.dataset = 2 #reset increment number if new filename

        if newOne >= 1 : # if a new dataset
            if clearDisplay == True: # clears the data display lists if new data & not just a renaming of previous data (overwrite protection)
                self.Forcelist.delete(0, 'end')
                self.Dislist.delete(0, 'end')
                self.Timelist.delete(0, 'end')
            words = len(filename.get())# number of letters in filename
            
            if self.dataset > 2: # if past 3rd dataset: erase previous incrementing value
                NumErase = len(str(self.dataset-2))# how many chars to erase from filename for incrementing
                self.entry_box.delete(words-NumErase, END)# deletes previous number from filename
                
            filename.set(filename.get()+str(self.dataset-1))# adds incremented number to filename

            #removes saving info text 
            self.DataSaved.place_forget()
            self.RawSaved.place_forget()
            self.AnotherOne.place_forget()
            self.NewName.place_forget()
            self.NewIncra.place_forget()
            self.NewIncra2.place_forget()
            self.Strength.place_forget()
            self.ScoreLab.place_forget()
            self.Score.place_forget()

        #Data collection buttons now displayed after 1st pressing of the 'New' button:
        #tells Arduino to start collecting data
        startB = tk.Button(self, text = "Start", font = ("arial", 16, "bold"), height = 3, width = 8, fg = "ghost white", bg = "gray2",command=lambda:self.start())
        startB.place(x = 675, y = 40)
        
        #tells Arduino to stop collecting data & saves the data (calls filename function)
        stopB = tk.Button(self, text = "Stop\n&\nSave", font = ("arial", 16, "bold"), height = 3, width = 8, fg = "ghost white", bg = "gray2",command=lambda:self.stop(filename))
        stopB.place(x = 675, y = 132)

        #tares/zeros load cell
        tareB = tk.Button(self, text = "Tare", font = ("arial", 16, "bold"), height = 3, width = 8, fg = "ghost white", bg = "gray2",command=lambda:self.tare())
        tareB.place(x = 675, y = 224)
        
        self.checkAutoGraph = tk.IntVar()
        self.checkAutoGraph.set(1)
        #on/off control of auto graph after stopping & saving data
        graphB = tk.Checkbutton(self, text = "Auto graph", variable = self.checkAutoGraph, width = 13, height = 2, bg = 'ghost white')
        graphB.place(x = 675 , y = 0)

        self.pastSet = self.dataset # records past dataset number
        self.prevName = filename.get() # records past filename
        
    # calls run function (for collecting Arduino data) to run in backend while GUI runs in frontend     
    def start(self):
        global collect # controls data collection loop
        collect = True # True = run the loop
        #global t1
        #print('isOpen ', ser.isOpen())
        #if ser.isOpen() == False:
         #   ser.open()
        #print(ser)
        # close initial serial port
        #print('')
        #print(' SERRR? ? ', ser)
        #serial = SerDisconnect(ser)
        #print('ser disconnect ', serial)
        #serial = SerConnect()
        #print('')
        #print('start ser ', ser)
        #Fb_center = barHeight.get() - .466 # corrects fb ruler measurement to actual fb center, originally was .5625 but it depends on tire pressure
        #Fb_center = barHeight.get() # CB 3/13/2022 # In 2021 the ruler was not used, and the ruler is risky.
        #self.Fb_bottom = Fb_center - .32 # Fb_center - radius of Fb (NOTE: depends on force bar height/radius)
        # For 2020 and 2021, we wrote down the wrong numbers, but the right numbers were saved to files
        #print("Fb center: ", Fb_center)
        #print("Fb bottom: ", self.Fb_bottom)
        #print(rows.get())

        #threading run function (simultaneously performs run function in backend)
        t1 = threading.Thread(target = run,args=(self, ser))
        t1.start()

    #zeroes load cell measurement
    def tare(self):
        ser.flush()#wait until all data is written
        tare = 't'
        ser.write(tare.encode()) #sends 't' to arduino, telling it to tare
        time.sleep(0.3)#wait x seconds for Arduino to tare load cell (for smoothing)

    #auto graph feature 
    def graph(self, dis, force, filename):
        if self.dataset-1 <= 1:
            self.legends = []
            
        if not plt.get_fignums():#if graph figure was closed, reset legend
            self.legends.clear()
            #print("new fig who dis")
        self.legends.append(filename.get())#add current filename to legend
        #fig = plt.figure(figsize=(8,4.8)) #fig size control 
        #plots force displacement graph
        plt.plot(dis, force)
        plt.xlabel("Distance (in.)")
        plt.ylabel("Force (lbs.)")
        plt.title(filename.get())
        plt.legend(self.legends)
        plt.axis = ([min(dis), max(dis), min(force), max(force)])
        
    def overwriteGuard(self, raw):# prevents overwriting by checking if filename already exists in saving folder

        return os.path.exists(raw) # True = already exits, False = doesn't exist
    
    # saves raw data in case of errors in processing of auto stats/graph save
    def saveRaw(self, filename):
        global clearDisplay # controls whether to clear Data display or not
        clearDisplay = True 
        
        # RAW data filename (adds 'RAW_' to the front)
        raw = address + '/RAW_' + (filename.get()) + '.xlsx'

        if self.overwriteGuard(raw) == True: # filename already exists, needs to be renamed
            self.dataset = self.dataset - 1 # don't increment data set
            clearDisplay = False # don't clear data display
            rename(filename.get()) # prompt user to rename file
            
        else:
            clearDisplay = True

        #try:   
        # Labels for Excel
        # ERROR CB FIX THIS JUNT
        dis = ["Distance (in.)"]
        force = ["Force (lbs.)"]
        elapsed = ["Time (s)"]

        #dis.append()
        
        cropHeight=["Height (in.)"]
        FbSetHeight=["Fb Middle Height (in.)"] # new, CB
        FbHeight=["Fb Bottom Height (in.)"]
        rowNum=["Rows"]
        stemNum=["Ave Stem Count"]
        countDis=["Sample Count Distance (in.)"]

        cropHeight.append(stemHeight.get()) # TypeError: 'float' object is not iterable
        FbSetHeight.append(barHeight.get()) # new, CB
        FbHeight.append(Fb_bottom)
        rowNum.append(rows.get())
        stemNum.append(stemCount.get())
        countDis.append(perDis.get())

        # new lists, with two values each
        stemNumLeft=["Left Sample Stem Count"]
        stemNumRight=["Right Sample Stem Count"]
        countDisStart = ["Sample Count Start Point (in.)"]
        countDisEnd = ["Sample Count End Point (in.)"]

        stemNumLeft.append(rowCountLeft.get())
        stemNumRight.append(rowCountRight.get())
        countDisStart.append(startCount.get())
        countDisEnd.append(endCount.get())
        

        # new lists to save, with more than two values each
        horzL = ["Horizontal Measurement Index (in.)"]
        StemHeightsMeasured = ["Stem Heights (in.)"]
        try:
            horzL.extend(Xa)
            StemHeightsMeasured.extend(Ha)
        except:
            print("Plot heights not input.")

        
        # open Excel worksheet
        workbook = xlsxwriter.Workbook(raw)
        worksheet = workbook.add_worksheet()

        # write Excel columns
        worksheet.write_column('A1', elapsed)
        worksheet.write_column('B1', dis)
        worksheet.write_column('C1', force)
        worksheet.write_column('D1', cropHeight)
        worksheet.write_column('E1', FbHeight)
        worksheet.write_column('F1', rowNum)
        worksheet.write_column('G1', stemNum)
        worksheet.write_column('H1', countDis)
        worksheet.write_column('I1', FbSetHeight)
        worksheet.write_column('J1', stemNumLeft)
        worksheet.write_column('K1', stemNumRight)
        worksheet.write_column('L1', countDisStart)
        worksheet.write_column('M1', countDisEnd)
        worksheet.write_column('N1', horzL)
        worksheet.write_column('O1', StemHeightsMeasured)
        
        
        # close workbook
        workbook.close()
        
        # remove labels for upcoming calculations
        dis.pop(0)
        force.pop(0)
        elapsed.pop(0)
        cropHeight.pop(0)
        stemNum.pop(0)
        countDis.pop(0)
        FbHeight.pop(0)
        rowNum.pop(0)

        # tell user raw data was saved
        self.RawSaved = tk.Label(self, text = "Raw data saved.", font = ("arial", 14, "bold"), fg = "dodgerblue2", bg = "ghost white")
        self.RawSaved.place(x=5, y = 90)

        try: 
            if max(dis) > 5 and generate_rich_files_toggle == 1: # checked if Encoder worked by making sure that the SOCEM traveled at least 5 inches
                self.calcs(filename)#run calcs function
        except:
            print("Push2")
        #except:
         #   errors.append('raw Excel writing') # error label
          #  eCode = 'e6'
           # errorCodes.append(eCode)  

    #Automatic stat calculation, INCLUDES EI ESTIMATIONS
    def calcs(self, filename):#Automated Calculations & Stats
        #try:
        # Crop Plot's distance estimations (need to remove force data where no contact with fb is made)
        i = 0
        while i <= (len(force)-1):#estimate distance of 1st contact w/ crops 
            if force[i] > 0.15: # once force rises above 0.15 
                hitD = dis[i] # record distance as plot's starting point
                startF = i # index for when to start looking at force (for mean)
                break # exit loop
            
            if i == len(force)-1: # if never reaches above 0.15 (due to distance measuring error), plot starts at 0
                hitD = 0
                startF = 0
            
            i = i + 1
        #print('1 out')
        
        j = 0
        for j in range(len(force)-1):# estimate distance point of plot's end
            if force[-j] > 0.15: # last instance force is above 0.15 
                doneD = dis[-j]
                lastF = -j # index for when to stop looking at force (for mean)
                break # exit loop
            
            if j == i: #(len(force)-2): # if never reaches above 0.15 (due to distance measuring error), use last dis & force pts
                doneD = dis[-1]
                lastF = force[-1]
                
        #Mean Force
        meanF.insert(0,"Mean Force (lbs.)")
        
        try:
            mean = sum(force[startF:lastF])/len(force[startF:lastF])
            meanF.insert(1, mean)
        except:
            mean = sum(force)/len(force)
            meanF.insert(1, mean) # store in list to save in Excel
            
        #Mean of Force values in range above the mean
        greatMean.insert(0, "Great Mean Force (lbs.)")
        forceArray = np.array(force) # convert force list to numpy array for quicker calcs
        greatForce = np.array(forceArray[forceArray > meanF[1]]) # create force array of values greater than overall mean
        gMean = np.mean(greatForce) # get "great" mean
        greatMean.insert(1, gMean) # store in list to save in Excel
        
        #Median/Percentiles
        medianF.insert(0, "Median Force (lbs.)")
        median = np.percentile(force, 50)
        medianF.insert(1, median)

        #Median w/o forces = 0
        medianPos.insert(0, "Positive Median F (lbs.)")
        try:
            medianPos.insert(1, np.percentile(force[startF:lastF], 50))
        except:
            medianPos.insert(1, np.percentile(force, 50))

        #Max Force 
        maxF.insert(0, "Max Force (lbs.)")
        maxed = max(force)
        maxF.insert(1, maxed)

        #Force per row list
        #print(forceArray)
        FpR = np.array(forceArray)/rows.get()
        #rowForce = FpR.tolist()
        for i in FpR:
            rowForce.append(i)
        rowForce.insert(0, 'Force/row (lbs.)')
        #for i in range(len(force)-1):
         #   rowForce.insert(i, force[i]/rows.get())

        # Ave force per row
        rowAve.insert(0, "Ave force/rows (lbs.)")
        rowAve.insert(1, np.mean(FpR))
        
        # Max force per row
        rowMax.insert(0, "Max force/rows (lbs.)")
        rowMax.insert(1, np.max(FpR))

        # stem density
        density.insert(0, "crops/in")
        density.insert(1, stemCount.get()/perDis.get())# crops/in.

        spacing.insert(0, "spacing (in.)")
        spacing.insert(1, 1/density[1]) # stem-to-stem spacing

        #ave. SOCEM velocity
        avelocity.insert(0, "Ave Velocity (ft./s)")
        avelo = dis[-2]/(12*elapsed[-2])
        avelocity.insert(1, avelo)

        #Sampling Rate
        sampling.insert(0,"Sampling Rate (Hz)")
        
        for i in range(len(elapsed)-1):
            change = elapsed[i+1] - elapsed[i]
            hz.insert(i, change)
 
        rate = sum(hz)/len(hz)
        sampling.insert(1,(1/rate))

        # Peak Forces/row Calcs:
        try: # try - in case peaks cannot be identified
            # only look at center of plot (to combat 'Edge Effect') - currently set to examine center 80 inches
            startDis = np.where(np.array(dis) >= 20)[0][0] # index where distance is about 20 inches into plot
            endDis = np.where(np.array(dis) <= 100)[-1][-1] # index where distance is 100 inches into plot
            
            fCenter = FpR[startDis:endDis]
            disCenter = np.array(dis[startDis:endDis])
            
            peaked = .15 # coefficient in peak definition (see peakutils library documentation) - needs fine-tuning
            minD = 70 # distance to check for peak (by indices?) - some tuning needed
            Fthresh = np.max(fCenter)*peaked # force per row peak definition
            PeakIndices = peakutils.indexes(fCenter, thres = Fthresh, min_dist = minD) # center plot peaks
            peakNum = 5 # number of top peaks to average from
            peakDescend = np.sort(fCenter[PeakIndices])# sort in descending order

            if len(peakDescend) > 5: # if more than 5 peaks, only look at top 5 peaks for mean
                topPeaks = peakDescend[-peakNum:len(peakDescend)]
                meanPeak = np.mean(topPeaks) # mean peak force
                
            else: # if less than 5 peak forces, average across all peak values
                topPeaks = peakDescend
                meanPeak = np.mean(peakDescend) # mean peak force

            EI_Inter = EI_Interaction_Fx.EI_Interaction(meanPeak, self.Fb_bottom, stemHeight.get(), spacing[1]) # compute EI assuming interactions
            EI_Non = EI_No_Interaction_Fx.EI_NoInteraction(meanPeak, self.Fb_bottom, stemHeight.get(), spacing[1]) # compute EI assuming no interactions
            EI_mean = (EI_Inter + EI_Non)/2
            EI_Interaction_Fx.clear_all() # ckear all arrays/lists for next calculation
            EI_No_Interaction_Fx.clear_all()
        except: # if error in peak finding process, indicate auto-calcs didn't process
            meanPeak = 'NA' 
            topPeaks = ['NA']  
            EI_Inter = 'NA' 
            EI_Non = 'NA' 
            EI_mean = 'NA'
            
        finally:
            avePeak.insert(0, 'Mean Peak Force/row (lbs.)')
            avePeak.insert(1, meanPeak)
            Peaks.insert(0, 'Top Selected Peaks (lbs.)')
            for i in topPeaks:
                Peaks.append(i)

            EII.insert(0, 'EI-Inter (lbs*in^2)')
            EIN.insert(0, 'EI-Non (lbs*in^2)')
            EIave.insert(0, 'Mean EI (lbs*in^2')
            EII.insert(1, EI_Inter)
            EIN.insert(1, EI_Non)
            EIave.insert(1, EI_mean)

            self.excel(filename)
      

    def excel(self, filename): # writes data with auto calcs to Excel file
        # Put labels back on for Excel
        # I guess this is fine? CB
        dis.insert(0, "Distance (in.)")
        force.insert(0, "Force (lbs.)")
        elapsed.insert(0 , "Time (s)")
        cropHeight.insert(0, "Height (in.)")
        FbHeight.insert(0, "Fb Bottom Height (in.)")
        rowNum.insert(0, "Rows")
        stemNum.insert(0, "Ave Stem Count")
        countDis.insert(0, "Sample Distance (in.)")
        
        f = address + '/' + (filename.get()) + ".xlsx" # address + filename

        workbook = xlsxwriter.Workbook(f)
        worksheet = workbook.add_worksheet('Plot_Data') # 1st sheet for plot data
        worksheet2 = workbook.add_worksheet('Row_Data_Calcs') # 2nd sheet for row data & auto-calcs
        worksheet3 = workbook.add_worksheet('SOCEM_Data') # 3rd sheet for SOCEM/user data
        # adjusting column widths
        # 1st sheet
        worksheet.set_column(0, 2, 12)
        worksheet.set_column(3, 3, 20)
        worksheet.set_column(4, 4, 12)
        worksheet.set_column(5, 5, 20)
        worksheet.set_column(6, 6, 8)
        worksheet.set_column(7, 7, 14)
        worksheet.set_column(8, 8, 17)
        worksheet.set_column(9, 9, 12)
        worksheet.set_column(10, 10, 14)
        # 2nd sheet
        worksheet2.set_column(0, 1, 14)
        worksheet2.set_column(2, 4, 23)
        worksheet2.set_column(5, 7, 15)
        # 3rd sheet
        worksheet3.set_column(0, 1, 16)

        # 1st sheet: plot data
        worksheet.write_column('A1', elapsed)
        worksheet.write_column('B1', dis)
        worksheet.write_column('C1', force)
        # Force stats
        worksheet.write_column('D1', meanF)
        worksheet.write_column('D4', medianF)
        worksheet.write_column('D7', medianPos)
        worksheet.write_column('D10', greatMean)
        worksheet.write_column('D13', maxF)
        worksheet.write_column('E1', cropHeight)
        worksheet.write_column('F1', FbHeight)
        worksheet.write_column('G1', rowNum)
        worksheet.write_column('H1', stemNum)
        worksheet.write_column('I1', countDis)
        # Crop density & spacing
        worksheet.write_column('J1', density)
        worksheet.write_column('K1', spacing)

        # 2nd sheet: row data & auto-calcs
        worksheet2.write_column('A1', dis)
        worksheet2.write_column('B1', rowForce)
        worksheet2.write_column('C1', rowAve)
        worksheet2.write_column('C4', rowMax)
        # Peak force per row
        worksheet2.write_column('D1', Peaks)
        worksheet2.write_column('E1', avePeak)
        
        # Auto EI estimations
        worksheet2.write_column('F1', EII)
        worksheet2.write_column('G1', EIN)
        worksheet2.write_column('H1', EIave)
        # User info (velocity & sampling rate)                       
        worksheet3.write_column('A1', avelocity)
        worksheet3.write_column('B1', sampling)
        
        l = len(dis) # used below

        # Plot force/row vs displacement scatter plot in Excel
        chart = workbook.add_chart({'type': 'scatter'})
        chart.set_x_axis({'name' : 'Distance (in.)'})
        chart.set_y_axis({'name' : 'Force/row (lbs.)'})
        chart.set_style(12)
        chart.set_size({'width': 520, 'height': 400})

        chart.add_series({'name': '=Row_Data_Calcs!$B1','categories': '=Row_Data_Calcs!$A$2:$A$'+str(l), 'values': '=Row_Data_Calcs!$B$2:$B$'+str(l),'marker':{'type': 'square','fill':{'color': 'black'},},})

        #Adds line indicating mean force/row & mean peak
        chartaves = workbook.add_chart({'type': 'line'})
        # mean force/row
        chart.add_series({'name': '=Row_Data_Calcs!$C1','categories': '=Row_Data_Calcs!$A$2:$A$'+str(l), 'values': '=Row_Data_Calcs!$C$2',
        'marker':{'type': 'diamond','fill':{'color': 'orange'},},'trendline': {'type': 'linear', 'line':{'color': 'orange',},},})
        # mean peak force
        chart.add_series({'name': '=Row_Data_Calcs!$E1','categories': '=Row_Data_Calcs!$A$2:$A$'+str(l), 'values': '=Row_Data_Calcs!$E$2',
        'marker':{'type': 'diamond','fill':{'color': 'red'},},'trendline': {'type': 'linear', 'line':{'color': 'red',},},})

        chart.combine(chartaves) # combines the plots (will generate Python warning)
        worksheet2.insert_chart('E4', chart) # positions the auto-graph in Excel file
    
        workbook.close()
        
        self.DataSaved = tk.Label(self, text = "Processed data saved.", font = ("arial", 14, "bold"), fg = "dodgerblue2", bg = "ghost white")
        self.DataSaved.place(x=5, y = 125)
       #self.namedfile = tk.Label(self,textvariable = filename,font = ("arial", 14, "bold"), fg = "dodgerblue2", bg = "ghost white")
        #self.namedfile.place(x = 146, y = 165)
                
        self.AnotherOne = tk.Label(self, text = "Ready for the next set of data.", font = ("arial", 14, "bold"), fg = "gray3", bg = "ghost white")
        self.AnotherOne.place(x = 5, y = 160)
        self.NewName = tk.Label(self, text = "Edit the filename as needed.", font = ("arial", 14, "bold"), fg = "gray3", bg = "ghost white")
        self.NewName.place(x = 5, y = 195)
        self.NewIncra = tk.Label(self, text = "'New' button now increments the filename", font = ("arial", 14, "bold"), fg = "gray3", bg = "ghost white")
        self.NewIncra.place(x = 5, y = 230)
        self.NewIncra2 = tk.Label(self, text = "if unchanged.", font = ("arial", 14, "bold"), fg = "gray3", bg = "ghost white")
        self.NewIncra2.place(x = 5, y = 260)
        self.Strength = tk.Label(self, text = "Strength", font = ("arial", 14, "bold"), fg = "gray3", bg = "ghost white")
        self.Strength.place(x = 520, y = 160)
        self.ScoreLab = tk.Label(self, text = "Score:", font = ("arial", 14, "bold"), fg = "gray3", bg = "ghost white")
        self.ScoreLab.place(x = 520, y = 190)
        sVal = EIave[1]
        #sVal = sVal.item()
        #print(sVal)
        #print(type(sVal))
        score = str('%.1f' % EIave[1])
        #print(score)
        self.Score = tk.Label(self, text = score, font = ("arial", 16, "bold"), fg = "dodgerblue2", bg = "ghost white")
        self.Score.place(x = 583, y = 188)
        
        #instant graph
        if self.checkAutoGraph.get() == 1:
            self.graph(dis[1:], force[1:], filename)
        
        #clear all data lists for next entry
            # Here is the problem. If the encoder fails, the data never gets cleared! CB
            # What problem? Months later, no idea what that guy is talking about. CB
        dis.clear()
        force.clear()
        elapsed.clear()
        cropHeight.clear()
        stemNum.clear()
        countDis.clear()
        meanF.clear()
        medianF.clear()
        medianPos.clear()
        greatMean.clear()
        maxF.clear()
        rowNum.clear()
        rowForce.clear()
        rowAve.clear()
        rowMax.clear()
        avelocity.clear()
        hz.clear()
        sampling.clear()
        aveHeight.clear()
        aveCount.clear()
        density.clear()
        spacing.clear()
        FbHeight.clear()
        Peaks.clear()
        avePeak.clear()
        EII.clear()
        EIN.clear()
        EIave.clear()
        
        filename = '' # issue?
       # EI_Interaction.clear_all()
       # EI_NoInteraction2.clear_all()

        plt.show()

    def stop(self,filename):
        try:
            ser.flushInput()# wait until all data is written
        except:
            print("Push")
        finally:
            global collect
            #stops data collection loop
            collect = False
        
        try:
            stopped = 'x'
            ser.write(stopped.encode())# sends 'x' to Arduino to stop reading sensors
            time.sleep(.5)# for potential error protection?
            #ser.close()
        except:
            errors.append('serial com. (stopping data)') # error label
            eCode = 'e7'
            errorCodes.append(eCode)  
        finally:
            print("File saved: ", str(filename.get()))
            self.saveRaw(filename)# run the Save Raw Data function (it then runs the Auto-Calcs function)
            self.dataset+=1 # increases the data set number 
            if self.dataset > 1: # updates 'New' button label to include increment
                incra = tk.Label(self, text = '(increment)', bg='gray2', fg = 'ghost white', font = ('arial', 12))
                incra.place(x = 575, y = 100)

            #print('stop isOpen ', ser.isOpen())      
            

# Load cell calibration page 
class Calibrate(tk.Frame):
    
    def __init__(self, parent, controller): # automatically runs
        
        tk.Frame.__init__(self, parent)
        
        # GUI design (text, user inputs (text input, buttons):
        header = tk.Label(self, text = "FORCE SENSOR CALIBRATION",
                          font = ("arial", 17, "bold"), fg = "gray3", bg="ghost white").place(x=235,y=0)

        tareIt = tk.Label(self, text = "1. Tare w/ no weight",
                          font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white").place(x=5,y=43)
        
        inputW = tk.Label(self, text = "2. Input weight (kg)",
                          font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white").place(x=5,y=73)
        
        caliIt = tk.Label(self, text = '3. Place weight',
                          font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white").place(x=5,y=103)

        caliIt = tk.Label(self, text = '4. Optimize so Diff. = 0',
                          font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white").place(x=5,y=133)

        testW = tk.Label(self, text = "Weight:",
                         font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white").place(x=5,y=183)

        self.knownW = tk.DoubleVar() # know weight textvariable
        self.knownW.set(0.0) # initially = 1.0 kg (assuming 1.0 kg will be used)
        knownWEntry = tk.Entry(self, textvariable=self.knownW,
               font = ("arial", 14, "bold"), width= 5, bg="white", fg="gray1").place(x = 80, y =183)

        kg = tk.Label(self, text = "kg",
                          font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white").place(x=140,y=183)

        self.lbs = self.knownW.get() * convert # convert known weight kg to lbs 
        self.strW = str('%.3f' % self.lbs) # store as string
        self.strLbs = tk.StringVar() # for displaying & updating on GUI
        self.strLbs.set(self.strW) # initial value = self.knownW

        eqLabel = tk.Label(self, text = '= ',
                          font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white").place(x=170,y=183)
        lbsLabel = tk.Label(self, textvariable = self.strLbs,
                          font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white").place(x=187,y=183)

        unitLabel = tk.Label(self, text = " lbs.",
                          font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white").place(x=249,y=183)
                
        caliLabel = tk.Label(self, text = "Cali. Factor:",
                          font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white").place(x=5,y=223)
    
        self.calibra = tk.IntVar() # needs to be int, not float
        self.calibra.set(199750) # initial calibration num. Has been working well
        self.factor = self.calibra.get() 
        self.calibraEntry = tk.Entry(self, textvariable=self.calibra,
               font = ("arial", 14, "bold"), width= 10, bg="white", fg="gray1")
        self.calibraEntry.place(x = 125, y = 223)

        #tares/zeros load cell
        tareB = tk.Button(self, text = "Tare", font = ("arial", 16, "bold"), height = 3, width = 8, fg = "ghost white", bg = "gray2",command=lambda:DataCollect.tare) # confirm this works
        tareB.place(x = 559, y = 44)

        # updates cali factor & starts/continues cali. process
        caliB = tk.Button(self, text ="Update\nCali.\nFactor",
                         font = ("arial", 16, "bold"), height = 3, width = 8, fg = "ghost white", bg = "gray2",
                         command=lambda:self.caliThread()).place(x = 675, y = 44)
        # stops cali. process
        doneB = tk.Button(self, text ="Done",
                         font = ("arial", 16, "bold"), height = 3, width = 8, fg = "ghost white", bg = "gray2",
                         command=lambda:self.doneCali()).place(x = 675, y = 224)

        # + 1000 to calibra
        p1000B = tk.Button(self, text ="+1000",
                         font = ("arial", 16, "bold"), height = 1, width = 8, fg = "ghost white", bg = "gray2",
                         command=lambda:self.updateCali(1000)).place(x = 559, y = 136)
        # - 1000 to calibra
        n1000B = tk.Button(self, text ="-1000",
                         font = ("arial", 16, "bold"), height = 1, width = 8, fg = "ghost white", bg = "gray2",
                         command=lambda:self.updateCali(-1000)).place(x = 559, y = 136+44)
        # + 100
        p100B = tk.Button(self, text ="+100",
                         font = ("arial", 16, "bold"), height = 1, width = 8, fg = "ghost white", bg = "gray2",
                         command=lambda:self.updateCali(100)).place(x = 675, y = 136)
        # - 100
        n100B = tk.Button(self, text ="-100",
                         font = ("arial", 16, "bold"), height = 1, width = 8, fg = "ghost white", bg = "gray2",
                         command=lambda:self.updateCali(-100)).place(x = 675, y = 136+44)

        scroll = tk.Scrollbar(self)

        self.LCLabel = tk.Label(self, text = "lbs.",font = ("arial", 14, "bold"), fg = "dodgerblue2", bg = "ghost white")
        self.LCLabel.place(x = 330, y = 43)
        self.LClist = tk.Listbox(self, yscrollcommand = scroll.set, bg = "ghost white",highlightbackground = "gray2", width = 7, height = 14, font = ("arial", 14, "bold"), fg = "dodgerblue2")
        self.LClist.place(x = 310, y = 73)

        self.DiffLabel = tk.Label(self, text = "Diff.",font = ("arial", 14, "bold"), fg = "dodgerblue2", bg = "ghost white")
        self.DiffLabel.place(x = 420, y = 43)
        self.Difflist = tk.Listbox(self, yscrollcommand = scroll.set, bg = "ghost white",highlightbackground = "gray2", width = 7, height = 14, font = ("arial", 14, "bold"), fg = "dodgerblue2")
        self.Difflist.place(x = 400, y = 73)

        HomeB = tk.Button(self, text ="Inputs",
                        font = ("arial", 16, "bold"), height = 3, width = 8, fg = "ghost white", bg = "gray2",
                        command=lambda:controller.show_frame(Home)).place(x = 0, y = 316)

        keyB = tk.Button(self, text = "Keyboard",
                       font = ("arial", 16, "bold"), height = 3, width = 8, fg = "ghost white", bg = "gray2",
                       command=keyboard).place(x = 675, y = 316)

    def updateCali(self, cali): # update calibration factor
        self.factor = self.calibra.get() + cali
        self.calibraEntry.delete(0, 'end')
        self.calibraEntry.insert(0, self.factor)
        return self.factor

    def tare(self):
        ser.flush()#wait until all data is written
        tare = 't'
        ser.write(tare.encode()) #sends 't' to arduino, telling it to tare
        time.sleep(0.3)#wait x seconds for Arduino to tare load cell (for smoothing)
       
    def caliFactor(self):
        self.lbs = self.knownW.get() * convert # convert known weight kg to lbs
        self.strW = str('%.3f' % self.lbs) # store as string
        self.strLbs.set(self.strW) # update GUI text
        
        scroll = tk.Scrollbar(self)
        self.factor = self.calibra.get() # get user input calibration factor
        self.doneCali() # if Arduino sending force data, this will momentarily stop it 
        
        strFactor = str(self.factor) # cali factor as string
        ser.write(strFactor.encode()) # send cali factor to Arduino
        ser.flush() # make sure it gets it before proceeding

        global caliLoop
        caliLoop = True
        #for i in range(20):
        #z = 0
        while caliLoop == True: # loop to continuously print Arduino force readings

            if ser.inWaiting() > 0: #checks to see if Serial is available 
                    
                try: #make sure serial data can be read/is there
                    ser_bytes = ser.readline()
                except:
                    errors.append('serial read')
                    eCode = 'e8'
                    errorCodes.append(eCode)
                    #popup("serial read")
                    
                bytesDecoded = (ser_bytes[0:len(ser_bytes)-2].decode("utf-8")) # force reading bytes
                #print(str(bytesDecoded))
                try:
                    reading = float(bytesDecoded) # convert bytes to float
                    diff = self.lbs - reading # difference between reading & known weight
                    #print(diff)
                    #print(reading)
                    #print(str('%.2f' % reading))
                    self.LClist.insert(END, str('%.2f' % reading)) # scrollbar list for force readings
                    self.Difflist.see(END)
                    self.Difflist.insert(END, str('%.1f' % diff)) # scrollbar list for forcebar - known weight 
                    self.LClist.see(END)
                except:
                    pass 

                #z+=1
                
    def caliThread(self): #threading calibrate function (simultaneously performs caliFactor function in backend)
        thread = threading.Thread(target = Calibrate.caliFactor,args=(self,))
        thread.start()

    def doneCali(self): # stops calibration process
        ser.reset_input_buffer()# clear the input buffer
        global caliLoop
        caliLoop = False # stop loop asking for data
        
        send = 'd'
        ser.write(send.encode()) # send 'd' to stop Arduino sending data
        
# error page for displaying errors
class ErrorReport(tk.Frame):

    def __init__(self, parent, controller): # automatically runs
        tk.Frame.__init__(self, parent)

        # button that returns to Geo. Inputs page/class
        HomeB = tk.Button(self, text ="Inputs",
                font = ("arial", 16, "bold"), height = 3, width = 8, fg = "ghost white", bg = "gray2",
                command=lambda:controller.show_frame(Home)).place(x = 675, y = 316)
        # button that returns to DataCollect page/class
        dataB = tk.Button(self, text = "Collect\nData",
                       font = ("arial", 16, "bold"), height = 3, width = 8, fg = "ghost white", bg = "gray2",
                       command=lambda:controller.show_frame(DataCollect)).place(x = 675, y = 225)
        
        scroll = tk.Scrollbar(self)
        
        self.ErrorCodeLabel = tk.Label(self, text = "Error Code\n(Location)",font = ("arial", 14, "bold"), fg = "gray3", bg = "ghost white").place(x = 179, y = 50)
        self.ErrorCodeList = tk.Listbox(self, yscrollcommand = scroll.set, bg = "ghost white",highlightbackground = "gray2", width = 10, height = 13, font = ("arial", 14, "bold"), fg = "dodgerblue2")
        self.ErrorCodeList.place(x = 175, y = 100)

        self.ErrorLabel = tk.Label(self, text = "Description",font = ("arial", 14, "bold"), fg = "gray3", bg = "ghost white")
        self.ErrorLabel.place(x = 400, y = 75)
        self.ErrorDesc = tk.Listbox(self, yscrollcommand = scroll.set, bg = "ghost white",highlightbackground = "gray2", width = 30, height = 13, font = ("arial", 14, "bold"), fg = "dodgerblue2")
        self.ErrorDesc.place(x = 289, y = 100)
        
    def showErrors2(self):

        self.ErrorCodeList.delete(0, 'end')
        self.ErrorDesc.delete(0, 'end')

        for e in range(len(errorCodes)):
            self.ErrorCodeList.insert(END, errorCodes[e])# inserts at end   of listbox to actually display
            self.ErrorCodeList.see(END)# makes sure listbox is at end so it displays live data
            self.ErrorDesc.insert(END, errors[e])
            self.ErrorDesc.see(END)

class Heights(tk.Frame):
    
    def __init__(self, parent, controller): # automatically runs

        tk.Frame.__init__(self, parent)

        Header = tk.Label(self, text = "Enter Heights Along Plot To Optimize Force Bar Height",
                          font = ("arial", 17, "bold"), fg = "gray3", bg="ghost white").place(x=50,y=0)

        Negatives = tk.Label(self, text = "*Negative values\n are converted\n to Null",
                          font = ("arial", 17, "bold"), fg = "gray3", bg="ghost white").place(x=5,y=60)

        xLabel = tk.Label(self, text = "x (in).",
                          font = ("arial", 17, "bold"), fg = "gray3", bg="ghost white").place(x=230,y=60)

        x1 = tk.DoubleVar()
        x1.set(20)
        x1Box = tk.Entry(self, textvariable=x1,
               font = ("arial", 14, "bold"), width= 6, bg="white", fg="gray1").place(x = 230, y = 90)

        x2 = tk.DoubleVar()
        x2.set(40)
        x2Box = tk.Entry(self, textvariable=x2,
               font = ("arial", 14, "bold"), width= 6, bg="white", fg="gray1").place(x = 230, y = 118)

        x3 = tk.DoubleVar()
        x3.set(60)
        x3Box = tk.Entry(self, textvariable=x3,
               font = ("arial", 14, "bold"), width= 6, bg="white", fg="gray1").place(x = 230, y = 118+28)

        x4 = tk.DoubleVar()
        x4.set(80)
        x4Box = tk.Entry(self, textvariable=x4,
               font = ("arial", 14, "bold"), width= 6, bg="white", fg="gray1").place(x = 230, y = 118+28+28)

        x5 = tk.DoubleVar()
        x5.set(100)
        x5Box = tk.Entry(self, textvariable=x5,
               font = ("arial", 14, "bold"), width= 6, bg="white", fg="gray1").place(x = 230, y = 118+(3*28))

        x6 = tk.DoubleVar()
        x6.set(120)
        x6Box = tk.Entry(self, textvariable=x6,
               font = ("arial", 14, "bold"), width= 6, bg="white", fg="gray1").place(x = 230, y = 118+(4*28))

        x7 = tk.DoubleVar()
        x7.set(-1)
        x7Box = tk.Entry(self, textvariable=x7,
               font = ("arial", 14, "bold"), width= 6, bg="white", fg="gray1").place(x = 230, y = 118+(5*28))

        x8 = tk.DoubleVar()
        x8.set(-1)
        x8Box = tk.Entry(self, textvariable=x8,
               font = ("arial", 14, "bold"), width= 6, bg="white", fg="gray1").place(x = 230, y = 118+(6*28))

        hLabel = tk.Label(self, text = "h (in).",
                          font = ("arial", 17, "bold"), fg = "gray3", bg="ghost white").place(x=330,y=60)

        h1 = tk.DoubleVar()
        h1Box = tk.Entry(self, textvariable=h1,
               font = ("arial", 14, "bold"), width= 6, bg="white", fg="gray1").place(x = 330, y = 90)

        h2 = tk.DoubleVar()
        h2Box = tk.Entry(self, textvariable=h2,
               font = ("arial", 14, "bold"), width= 6, bg="white", fg="gray1").place(x = 330, y = 118)

        h3 = tk.DoubleVar()
        h3Box = tk.Entry(self, textvariable=h3,
               font = ("arial", 14, "bold"), width= 6, bg="white", fg="gray1").place(x = 330, y = 118+28)

        h4 = tk.DoubleVar()
        h4Box = tk.Entry(self, textvariable=h4,
               font = ("arial", 14, "bold"), width= 6, bg="white", fg="gray1").place(x = 330, y = 118+28+28)

        h5 = tk.DoubleVar()
        h5Box = tk.Entry(self, textvariable=h5,
               font = ("arial", 14, "bold"), width= 6, bg="white", fg="gray1").place(x = 330, y = 118+(3*28))

        h6 = tk.DoubleVar()
        h6Box = tk.Entry(self, textvariable=h6,
               font = ("arial", 14, "bold"), width= 6, bg="white", fg="gray1").place(x = 330, y = 118+(4*28))

        h7 = tk.DoubleVar()
        h7.set(-1)
        h7Box = tk.Entry(self, textvariable=h7,
               font = ("arial", 14, "bold"), width= 6, bg="white", fg="gray1").place(x = 330, y = 118+(5*28))

        h8 = tk.DoubleVar()
        h8.set(-1)
        h8Box = tk.Entry(self, textvariable=h8,
               font = ("arial", 14, "bold"), width= 6, bg="white", fg="gray1").place(x = 330, y = 118+(6*28))

        #button that calculates optimized force bar height
        optiB = tk.Button(self, text ="Optimize\n Force Bar",
                        font = ("arial", 16, "bold"), height = 3, width = 8, fg = "ghost white", bg = "gray2",
                        command=lambda:self.optiH([x1.get(), x2.get(), x3.get(), x4.get(), x5.get(), x6.get(), x7.get(), x8.get()],
                                                  [h1.get(), h2.get(), h3.get(), h4.get(), h5.get(), h6.get(), h7.get(), h8.get()])).place(x = 410, y = 90)

        #button that goes back to 1st page (Inputs / home)
        HomeB = tk.Button(self, text ="Inputs",
                        font = ("arial", 16, "bold"), height = 3, width = 8, fg = "ghost white", bg = "gray2",
                        command=lambda:controller.show_frame(Home)).place(x = 0, y = 316)

        
        keyB = tk.Button(self, text = "Keyboard",
                       font = ("arial", 16, "bold"), height = 3, width = 8, fg = "ghost white", bg = "gray2",
                       command=keyboard).place(x = 675, y = 316)

    def optiH(self, X, H):
        global Xa, Ha
        Xa = [] # x non-null list, horzL
        Ha= [] # H non-null list, xStemHeights
        for i in range(len(X)):
            if X[i] > 0:
                Xa.append(X[i])
                Ha.append(H[i])

        global aveH, Fb_place, Fb
        aveH = np.mean(Ha)
        step = 0.5
        Fb = optiH.optiH(Xa, Ha, step)
        #print(Fb)
        # Fb_plae = user will set force bar to this height (as measured by SOCEM wood ruler) 
        # Fb_place = float(Fb[0]) + .466 + .32  # Fb + correction distance + fb radius # SEE force bar input code (around line 545)
        # fb values should have been legitimate without correct.
        Fb_place = float("%.4f" % float(Fb[0]))
        print("Fb_place = ", str(Fb_place))

        # has the friggin wooden ruler offset build in - fix this!!!! CB
        
        Fb1Label = tk.Label(self, text = "Force Bar Height: ",
                          font = ("arial", 17, "bold"), fg = "gray3", bg="ghost white").place(x=410,y=190)

        FbLabel = tk.Label(self, text = Fb_place,
                          font = ("arial", 17, "bold"), fg = "dodgerblue2", bg = "ghost white").place(x=605,y=190)

        hScoreLab = tk.Label(self, text = "Score:",
                          font = ("arial", 17, "bold"), fg = "gray3", bg="ghost white").place(x=410,y=220)

        hScore = tk.Label(self, text = Fb[2],
                          font = ("arial", 17, "bold"), fg = "dodgerblue2", bg = "ghost white").place(x=485,y=220)

        best= tk.Label(self, text = "(best = 1.0)",
                          font = ("arial", 17, "bold"), fg = "gray3", bg="ghost white").place(x=550,y=220)

        ratioLab = tk.Label(self, text = "Avg. h/l:",
                          font = ("arial", 17, "bold"), fg = "gray3", bg="ghost white").place(x=410,y=250)

        ratio = tk.Label(self, text = Fb[1],
                          font = ("arial", 17, "bold"), fg = "dodgerblue2", bg = "ghost white").place(x=520,y=250)

        aveHLab = tk.Label(self, text = "Avg. h:",
                          font = ("arial", 17, "bold"), fg = "gray3", bg="ghost white").place(x=410,y=280)

        aveHv = tk.Label(self, text = "%.2f " % aveH,
                          font = ("arial", 17, "bold"), fg = "dodgerblue2", bg = "ghost white").place(x=500,y=280)

        # need way to return these results such that they can be saved and passes on, CB
        return Xa, Ha, aveH, Fb
    #global Xa, Ha, aveH, fB

        
 # Guide page 
class Guide(tk.Frame):
    
    def __init__(self, parent, controller): # automatically runs

        tk.Frame.__init__(self, parent)
        
        guideHeader = tk.Label(self, text = "GUIDE",
                          font = ("arial", 17, "bold"), fg = "gray3", bg="ghost white").place(x=350,y=0)

        # instruction steps:
        one = tk.Label(self, text = "1. Position SOCEM as shown",
                          font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white").place(x=5,y=30)

        two = tk.Label(self, text = "2. Clear any debris in plot",
                          font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white").place(x=5,y=56)

        three = tk.Label(self, text = "3. Adjust forcebar to 70-90% stem height",
                          font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white").place(x=5,y=81)
        
        four = tk.Label(self, text = "4. Enter all required inputs.",
                          font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white").place(x=5,y=106)
        
        four = tk.Label(self, text = '5. Press "Collect Data" button',
                          font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white").place(x=5,y=131)

        five = tk.Label(self, text = '6. Enter filename for new dataset',
                          font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white").place(x=5,y=156)

        six = tk.Label(self, text = '6. Press "New" & then "Start" buttons',
                          font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white").place(x=5,y=181)
        
        seven = tk.Label(self, text = "7. Slowly & steadily push SOCEM through plot",
                          font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white").place(x=5,y=206)
        
        eight = tk.Label(self, text = '8. Press "Stop&Save" button',
                          font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white").place(x=5,y=231)

        nine = tk.Label(self, text = '9. Press "New" and rename for next data file',
                          font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white").place(x=5,y=256)

        ten = tk.Label(self, text = '10. Repeat 5.-9.',
                          font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white").place(x=5,y=281)

        '''
        # SOCEM diagram of use 
        load = PIL.Image.open('SOCEM.png')
        render = PIL.ImageTk.PhotoImage(load)
        img = tk.Label(self, image=render)
        img.image = render
        img.place(x = 480, y = 65)
        '''

        #button that goes back to 1st page (Inputs / home)
        HomeB = tk.Button(self, text ="Inputs",
                        font = ("arial", 16, "bold"), height = 3, width = 8, fg = "ghost white", bg = "gray2",
                        command=lambda:controller.show_frame(Home)).place(x = 0, y = 316)

if __name__ == "__main__":
    # INITIATES GUI TO START
    #root= tk.Tk() # added CB
    app = GUI()
    #ser = SerConnect()
    b = DataCollect(app,tk.Frame)
    fig = plt.figure()
    #global filename
    #filename = tk.StringVar()
    #c = named(app, tk.Frame)
    app.title("StemBerry")
    app.geometry("800x480+0+0")
    #app.iconbitmap(s'/home/pi/Desktop/SOCEM Code')
    #full screen:
    #app.geometry("{0}x{1}+0+0".format(app.winfo_screenwidth()-3,app.winfo_screenheight()-3))
    app.mainloop()
        

