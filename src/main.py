#!/usr/bin/python3
#do not erase (needed to be executable for autostart)

'''
StemBerry V.105
Last updated: 10/16/2022
Dev: Clayton Bennett
OG dev: Austin Bebee
Description: SOCEM GUI. Connect RPi to Arduino, collect raw data. Save text inputs.

Contents (in order):s
- Library imports
- Global Variables
- Global Functions
- GUI Class
    - Home / Initial input screen
    - Data collection (Record Force) screen
        - Runs data collection function
        - Stores data & saves data
        - Plots F v D graph
    - Load cell calibration screen
    - Error report screen
- Excute GUI command

V15
    - Change to 9 cell and 3 range count inputs
V19
    - Rip out defunct calculations
    - Clean up code, specifically by organizing statements of place for tkinter items
V37
    - Dial in functionality with pretty new GUI.
    - barbottom (not barmiddle) set to 70%-90% of stem height
V42
    - Develop top level methods
V50
    - Functional save state, save files, naming convention edge cases, and crisp appearance

V54
    - Generate CSV's, suppress XLSX's
V56
    - Retain 9-cell variables, for EI assessment upon saving counts, without reopening CSV files
V67
    - So many things.
v77
    - Serial collection functial, drinking from a waterhose, high hz
    - Tare button message.
    - PeakClick popup window.

V84
    - The way peak clicks are handled and saved was moved to the inside of the choose peaks code, becuase plt.show() won't give up.
    - Shut down plt.show after CSV file is saved.
V88
    - GUI.filename_force updated on page change to either record force frame or final inputs page
    - nameBlackBox updated to remove excess hyphen when direction ==''
    - XLSX compilation file functional, currently set to seek force and EI files
    - EI calcualtion works - only needs 1 file for all four nine-cell-scheme tests. 
    - This thing is getting heavy, 2844 lines.
V90
    - Identify OS and choose filepath accordingly.

V92
    - Trigger peak selection for all tests, with the assessAllTests boolean.
    - Noticed that encoderWorked_override is poorly implemented. No reason to fix now, but, should be alterable as opposed to needing manual suppression through commenting
    - GUI.currentdirection.get() set to "" on_frame_show RecordForce.
V94
    - Changed mass measurement from kg to gramsa
    - Fixed all time units to be (sec), not (s) or (seconds), and certainly not (ms)
V96
    - EI is now calculated in lbs*in^2, then converted to metric N*cm^2. Input is metric, conversion happens inside, processing is SAE, then conversion to metric before output to metric.
V97
    - EI calculation betaV edge cases dealt with: if nan, set betaV to 0.
v99
    - Change if statement in serConnect to retain dev_manual
Fix:
- Change compilation to access CVSV data rather than state data. This is to protect against data loss if the computer dies.
- Or, load state. Load state would be sick.
- Add more variables to state save backup text file.
- Remove auto graph button, or at least uncheck it: use it to refer to auto clicker
- Finish autoclicker by setting plt.show() into an inset tkinter gui popup, and then mainoop.
     Use: FigureCanvasTkAgg,NavigationToolbar2Tk,plt,Cursor.
- dev port is currently defined manually, given dev_manualOverride
- move header variable inputs
- make directory inputtable using dropdown menu item and textbox
- upgrade tkinter items to CustomTkinter
- PRIORITY: CREATE BASE NAME FROM VARIABLE AND PLOT: GUI.filename_force.get() is getting dangerous.
     
Notes:
- exec() is your friend. Use is to run multiple lines of code which you can copy and paste into a shell, using triple '  commenting
- save as separate CSV files, then as one combined XLSX file with multiple pages
'''

'''Local libraries'''
import src.cursor
from src.guiframe_final_inputs import FinalInputs
import src.serial

''' Libraries '''
import tkinter as tk
from multiprocessing import Process

import matplotlib
from matplotlib import style
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import sys
import os
import platform
from os import path
import numpy as np
import pandas as pd
#import peakutils
#from PeakUtils.Plot import plot as pplot
import math
#import struct # what is this?
import datetime
from datetime import date
import time
import xlsxwriter

''' Global Variables --> Config'''

operator = 'Clayton Bennett'
location = 'EP425' # 'Kambitsch Farm'
coordinates = '46.592516,-116.946268'
script = os.path.basename(__file__)
directory = os.path.dirname(__file__)
operatingsystem = platform.system() #determine OS
# use or sys.plaform instead of platform.system, to avoid importing platform
print("operatingsystem =",operatingsystem)
print("os.getlogin() =",os.getlogin())
print("operator =",operator)
print("location =",location)
today = date.today()
datestring = today.strftime("%b-%d-%Y")
ignoreserial = False # True 
#ignoreserial = True # delete this # if RecordForce.ser.isOpen() == False:
barlength = 76 # cm. this shouldn't ever change, unless the bar is replaced. i.e. the width of a side hit cell.
#dev_manual = 'COM7' # manual override
dev_manual = '/dev/ttyACM0' # manual override
#dev_manual = 'COM7' # manual override
dev_manualOverride = True
useInitialPlot_PeackClick = False
distance_referenced_PeakClick = False
barradius = .8 # 1 cm = 0.32 inches
#barradius = 1 # 1 cm = 0.32 inches
default_stemheight = 10.0 # cm
initial_barbottomOverStemheight_coeff = 0.8
convert_KgToLbs = 2.20462262 #kg to lbs
convert_KgToN = 1/9.81 #kg to N # CHECK FOR ACCURACY CB 8/9/2022
convert_NToLbs = 4.44822
#calibrationFactor = 199750 # 23.4 N > 5 lbs; 5 lbs = 22.2411
calibrationFactor = 204200 # 22.24 N = 5 lbs

inchonvert = (((math.pi*(0.764))*31.4136)/359) # converts displacement to inches, wheel diameter = 31.4136
visualizeDatastream = False #True #set to live graph for data display
sleepSend = 0.5
encoderWorked_override = False # False means encoder will be trated as not working. this is poor code and should be improved.
assessAllTests = True
refreshAllAuto = False
autopopulatestemcount = True
defaultstemcount = 33
importFileDataTF = True
#visualizeDatastream = True
# visualizeDatastream ( search: "def datafeed(" ) is broken right now. Refer to earlier versions (pre v65)for reference of how Bebee left it.
vis = 's' # legacy
vis = 'nope' # 

if operatingsystem == 'Windows':
    if os.getlogin() == 'clayt':
        address = r'C:\Users\clayton\OneDrive - University of Idaho\AqMEQ\SOCEM\Data - Instron and SOCEM - 2020, 2021\SOCEM_DATA_2021'
        dev_guess = 'COM3' # manual override, windows 10 OS
    else:
        #dev_manualOverride = False
        address = directory + '/SOCEM_data'
        if not os.path.exists(address):
            os.makedirs(address) 
elif operatingsystem == 'Linux':
    dev_guess = '/dev/ttyACM0' # manual override raspian OS
    address = '/home/pi/Desktop/SOCEM_data_2022'
else:
    address = directory + '/SOCEM_data'
    dev_guess = dev_manual
    dev_manualOverride = False
    if not os.path.exists(address):
        os.makedirs(address)
        
''' matplotlib Graph Settings '''
'''
style.use("ggplot")
f = Figure(figsize=(4.85,3.9), dpi=75)
a = f.add_subplot(111)
a.set_ylim(0, 25)
'''

''' Methods'''


def overwriteGuard(filename):# prevents overwriting by checking if filename already exists in saving folder
        return path.exists(filename) # True = already exits, False = doesn't exist
    
def overwriteGuardPage(filename):# prevents overwriting by checking if filename already exists in saving folder
        #return path.exists(filename) # True = already exits, False = doesn't exist
        return False # don't mess up!
    
def data_display(visual): #changes display method    #DELETE?
    global visualizeDatastream
    visualizeDatastream = visual
    return visualizeDatastream

#if any error occurs, display popup error msg
def popup(error):
    popup = tk.Tk()
    popup.wm_title("Error")
    E_label = tk.Label(popup, text="A {} error occurred.".format(error), font=("arial", 12, "bold"))
    E_label.pack(side="top", fill="x", pady=10)               
    popup.mainloop()

def popup_chooseFolder():
    popup_chooseFolder = tk.Tk()
    popup_chooseFolder.wm_title("Choose Folder")
    E_label = tk.Label(popup_chooseFolder, text="Paste file output directory here.", font=("arial", 12, "bold"))
    #E_label.pack(side="top", fill="x", pady=10)
    E_label.grid(row=0, column=1)
    #GUI.addressInput.set("")
    folder_entry = tk.Entry(popup_chooseFolder, textvariable=GUI.addressInput, font = ("arial", 11, "bold"), width= 70, bg="white", fg="gray1")
    folder_entry.grid(row=1, column=1)
    save_button = tk.Button(popup_chooseFolder,text = "Save", font = ("arial", 14, "bold"), height = 1, width = 6, fg = "ghost white", bg = "dodgerblue3",command=lambda:updateAdress())
    save_button.grid(row=2, column=1)
    popup_chooseFolder.mainloop()
    
    ''' Frame: Folder Input Field''
    barset_frame = tk.LabelFrame(self, text='Bar Bottom Quickset',font = ("arial", 14, "bold"), width= 10, bg="white", fg="gray1")
    barset_frame.place(x = 340, y = 230)
    ''' ''

def updateAdress():
    print("updateAddress is broken. Please develop.")
    print("GUI.addressInput.get() = ",GUI.addressInput.get())
    print("GUI.address = ",GUI.address)
    #GUI.address = GUI.addressInput.get() # broken right now
    #print("GUI.address = ",GUI.address)

def showErrors():
    GUI.show_frame(ErrorReport) # show Error Report page
    ErrorReport.showErrors2(GUI.frames[ErrorReport]) # display errors in lists

def update_filename_preTest():
    filename_preTest = nameBlackBox("preTest",GUI.filename_preTest.get())
    GUI.filename_preTest.set(filename_preTest)
    filename_all = filename_preTest.replace("preTest","all")
    GUI.filename_all.set(filename_all)

def testForNineCellFilename(): # used to identify when nine-cell force, distance, and time data exists, and passes it to state data.
    # the purpose of this is to avoid reopening CSV files in order to assess nine-cell data
    # because, we have to wait for counts after to assess EI
    # it would be easier to test right away to get peaks
    # have a check box for nine cell test
    # EI cannot be assessed for non-nine cell, because counts don't exist
    # if box not checked, post test frame goes to single input for stem count, one number, with another number for range distance of count
    # # Assessment is trigged at save state button push
    #ninecellfilename = GUI.varietyname.get()+","+GUI.plotname.get()+"_"
    ninecellfilename = GUI.varietyname.get()+","+GUI.plotname.get()
    ninecellfilename_side1 = ninecellfilename+"_side1"
    ninecellfilename_side2 = ninecellfilename+"_side2"
    ninecellfilename_side3 = ninecellfilename+"_side3"
    ninecellfilename_forward = ninecellfilename+"_foward"
    currentFilename_force = GUI.filename_force.get()
    # create GUI variable, for handling without reopening CSV's
    #if (currentFilename_force == ninecellfilename_side1):
    if (GUI.currentdirection.get() == "side1"):
        GUI.forcePushed_side1 = GUI.forcePushed
        GUI.distanceTraveled_side1 = GUI.distanceTraveled
        GUI.timeElapsed_side1 = GUI.timeElapsed
        #if (currentFilename_force == ninecellfilename_side2):
    if (GUI.currentdirection.get() == "side2"):
        GUI.forcePushed_side2 = GUI.forcePushed
        GUI.distanceTraveled_side2 = GUI.distanceTraveled
        GUI.timeElapsed_side2 = GUI.timeElapsed
        #if (currentFilename_force == ninecellfilename_side3):
    if (GUI.currentdirection.get() == "side3"):
        GUI.forcePushed_side3 = GUI.forcePushed
        GUI.distanceTraveled_side3 = GUI.distanceTraveled
        GUI.timeElapsed_side3 = GUI.timeElapsed
        #if (currentFilename_force == ninecellfilename_forward):
    if (GUI.currentdirection.get() == "forward"):
        GUI.forcePushed_forward = GUI.forcePushed
        GUI.distanceTraveled_forward = GUI.distanceTraveled
        GUI.timeElapsed_forward = GUI.timeElapsed
    


def rename(filename): #if filename already exists - prompt user to rename
    popup = tk.Tk()
    popup.wm_title('Prompt Rename')
    renameIt = tk.Label(popup, text = 'Filename\n"{}"\nalready exists in the saving location.\nPlease rename and press Save.'.format(filename), font = ('arial', 10, 'bold'))
    increment_button = tk.Button(popup,text = "Auto Modify", font = ("arial", 14, "bold"), height = 2, width = 6, fg = "ghost white", bg = "dodgerblue3",command=lambda:incrementRename(filename))
    overwrite_button = tk.Button(popup, text = "Overwrite", font = ("arial", 14, "bold"), height = 2, width = 6, fg = "ghost white", bg = "red4",command=lambda:overwrite(filename))
    
    
    renameIt.pack(side='top', fill='x', ipadx=10, ipady=10)
    increment_button.pack(side='top', fill='both', ipadx=10, ipady=1)
    overwrite_button.pack(side='top', fill='both', ipadx=10,ipady=1)

    popup.mainloop()
def renamePage(filename):
    print("Please develop, prevent pages from being overwritten in the filename_all spreadsheet")
    
def incrementRename(filename):
    print("please develop, auto modify filename")
    
def overwrite(filename):
    print("please develop, overwrite filename")
        
#closes GUI (from file menubar)
def close():
    createBackupFile()
    python = sys.executable
    os.execl(python, python, * sys.argv)



def incrementName(filename):
        hyphen = "_"
        # determine last few characters from a filename
        def incrementvars(filename):
            lastchar = filename[len(filename)-1]
            secondtolastchar = filename[len(filename)-2]
            thirdtolastchar = filename[len(filename)-3]
            lastcharandsecondtolastchar = str(secondtolastchar+lastchar)
            return lastchar, secondtolastchar, thirdtolastchar, lastcharandsecondtolastchar

        #check if the last two are hyphens. if there is more than one hypthen, remove the last character until there is only one hyphen.
        def hyphencheck(filename,hyphen,lastchar, secondtolastchar, thirdtolastchar, lastcharandsecondtolastchar):
            while lastchar == hyphen and secondtolastchar == hyphen: # if two hyphens at the end
                filename = filename[:-1] # remove last character
                incrementvars()
            return filename, lastchar, secondtolastchar, thirdtolastchar, lastcharandsecondtolastchar

        if filename == "": # default, if user tried to increment without inputting any varietyname, plotname, or filename
            filename = datestring+","+GUI.timestring.get()
            
        lastchar, secondtolastchar, thirdtolastchar, lastcharandsecondtolastchar = incrementvars(filename)
        filename, lastchar, secondtolastchar, thirdtolastchar, lastcharandsecondtolastchar = hyphencheck(filename,hyphen,lastchar, secondtolastchar, thirdtolastchar, lastcharandsecondtolastchar)
        
        if lastchar == hyphen: # if last character is a hyphen
            newName = str(filename+str("1"))
        elif secondtolastchar == hyphen and lastchar.isnumeric: # if single digit preceded by a hyphen
            #newName = str(filename+str(int(lastchar)+1))
            filename = filename[:-1] # remove last character
            newName = str(filename+str(int(lastchar)+1))
        elif thirdtolastchar == hyphen and lastcharandsecondtolastchar.isnumeric: # if double digits preceded by a hyphen
            filename = filename[:-1] # remove last character
            filename = filename[:-1] # remove last character
            newName = str(filename+str(int(lastcharandsecondtolastchar)+1))
        elif filename == "":
            newName = date
        else:
            newName = str(filename+"_1")
        return newName
        #GUI.filename_force.set(newName)
    
''' Edge cases: Filenaming '''
def nameDirectionScrub(filename):
    if ("_side1" in filename):
        filename=filename.replace("_side1","")
        print(filename)
    if ("_side2" in filename):
        filename=filename.replace("_side2","")
    if ("_side3" in filename):
        filename=filename.replace("_side3","")
    if ("_forward" in filename):
        filename=filename.replace("_forward","")
    if ("_postTest" in filename):
        filename=filename.replace("_postTest","")
    return filename

def nameMissing(varietyname,plotname):
    if varietyname == "":
        varietyname = datestring
    if plotname == "":
        plotname = GUI.timestring.get() # plotname = GUI.timestring.get() # if you want the timestring (serving at plotname) to not change...but then it will never change
    return varietyname, plotname

def nameBlackBox(direction,filename):
    varietyname = GUI.varietyname.get()
    plotname = GUI.plotname.get()
    check=GUI.passfillednames_checkbox.get()
    if GUI.filename_force.get()=="" and check==1 and direction=='':
        varietyname, plotname = nameMissing(varietyname, plotname)
        #print(varietyname, plotname)
        filename = str(varietyname+str(",")+plotname)
    elif GUI.filename_force.get()=="" and check==1 and direction!='':
        varietyname, plotname = nameMissing(varietyname, plotname)
        filename = str(varietyname+str(",")+plotname+"_"+direction)
    elif GUI.filename_force.get()=="" and check==0 and direction !='':
        filename = datestring+","+time.strftime("%H%M")+"_"+direction
    elif GUI.filename_force.get()!="" and check==1 and direction !='':
        varietyname, plotname = nameMissing(varietyname, plotname)
        filename = str(varietyname+str(",")+plotname+str("_")+direction)
    elif GUI.filename_force.get()!="" and check==0 and direction !='':
        if ("side1" in filename) or ("side2" in filename) or ("side3" in filename) or ("forward" in filename) or ("postTest" in filename):
            filename = nameDirectionScrub(GUI.filename_force.get())
            filename = filename+"_"+direction
        else:
            filename = filename+"_"+direction
    elif GUI.filename_force.get()=="" and check==0 and direction =='':
        filename = datestring+","+time.strftime("%H%M")
    elif GUI.filename_force.get()!="" and check==1 and direction =='':
        varietyname, plotname = nameMissing(varietyname, plotname)
        filename = str(varietyname+str(",")+plotname)
    elif GUI.filename_force.get()!="" and check==0 and direction =='':
        if ("side1" in filename) or ("side2" in filename) or ("side3" in filename) or ("forward" in filename) or ("postTest" in filename):
            filename = nameDirectionScrub(GUI.filename_force.get())
            filename = filename
        else:
            filename = filename
    #GUI.filename_postTest.set(filename_postTest)
    return filename
''' end: Edge cases: Filenaming '''

''' Single XLSX workbook created from all expected CSV files for 9-cell study'''
def generateXSLXcombinedFile():
    writer = pd.ExcelWriter('default.xlsx')
    for csvfilename in sys.ar[1:]:
        df = pd.read.csv(csvfilename)
        #FIX df.to_excel(writer.sheet_names=os.path.splitext(csvfilename)[0]) # "keyword cannot be an expression"
    writer.save()
    
def peakClickRunAndSave(filename):
    PeakClick() # you cannot put in counts first....because they haven't been collected yet!
    #ergo, run clicks after triggered XLSX workbook creation
''' trigger with button, on Initial Inputs page. Button also clears all data from stemberry, wait it dods not triggers PeakClick.py, which saves to a separate CSV before all CSV's are wrapped into a xlsx workbook.
'''

#Bebee legacy
# * # DATA COLLECTION FUNCTION - Acquires live data from Arduino # * #
def run(self, ser):
    try:        
        started = 's'
        ser.write(started.encode()) #sends 's' to arduino, telling it to start
        print('send s to arduino, legacy')
    except:
        errors.append('serial com. (start data)') # label 
        eCode = 'e2'
        errorCodes.append(eCode)
        popup('start data collect')
        
    ser.flush()
    time.sleep(.1)
    #Don't need this:
    #try:
    #ser_bytes = ser.readline()
    #decoded_bytes.insert(0,(ser_bytes[0:len(ser_bytes)-2].decode("utf-8")))#translates bytes to string, inserts incoming data in decoded_bytes list
    #except:
     #  popup("communication")

    #DATA COLLECTION CODE

    if vis == 's':# data displayed in scrollbars (default)
        # Displays incoming data 
        scroll = tk.Scrollbar(self)

        RecordForce.timeLabel = tk.Label(self, text = "s",font = ("arial", 14, "bold"), fg = "dodgerblue2", bg = "ghost white")
        RecordForce.timeLabel.place(x = 274, y = 70)
        RecordForce.Timelist = tk.Listbox(self, yscrollcommand = scroll.set, bg = "ghost white",highlightbackground = "gray2", width = 7, height = 1, font = ("arial", 14, "bold"), fg = "dodgerblue2")
        RecordForce.Timelist.place(x = 240, y = 100)

        RecordForce.disLabel = tk.Label(self, text = "in.",font = ("arial", 14, "bold"), fg = "dodgerblue2", bg = "ghost white")
        RecordForce.disLabel.place(x = 357, y = 70)
        RecordForce.Dislist = tk.Listbox(self, yscrollcommand = scroll.set, bg = "ghost white",highlightbackground = "gray2", width = 7, height = 1, font = ("arial", 14, "bold"), fg = "dodgerblue2")
        RecordForce.Dislist.place(x = 330, y = 100)

        RecordForce.forceLabel = tk.Label(self, text = "lbs.",font = ("arial", 14, "bold"), fg = "dodgerblue2", bg = "ghost white")
        RecordForce.forceLabel.place(x = 444, y = 70)
        RecordForce.Forcelist = tk.Listbox(self, yscrollcommand = scroll.set, bg = "ghost white",highlightbackground = "gray2", width = 7, height = 11, font = ("arial", 14, "bold"), fg = "dodgerblue2")
        RecordForce.Forcelist.place(x = 420, y = 100)

    else:# user decided for no data display
        try:#clear scrollbars if they were there
            RecordForce.Dislist.place_forget()
            RecordForce.Forcelist.place_forget()
            RecordForce.Timelist.place_forget()
            RecordForce.disLabel.place_forget()
            RecordForce.forceLabel.place_forget()
            RecordForce.timeLabel.place_forget()
        except:# no scrollbars
            print("no scrollbars")
            pass
    
    i = 0
    print("i = 0")
    RecordForce.elapsed = []
    RecordForce.dis = []
    RecordForce.force = []
    string = list()

    #try:
    
    while RecordForce.collect == True: # GUI in frontend controls value of collect to start/stop loop            
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
            #print("bytesDecoded = ",bytesDecoded)
            string.insert(i,str(bytesDecoded)) # inserts decoded bytes into string
            #print(' run ser read ', string[i]) # useful debugging tool
            split = string[i].split("|") # splits data at | (1st = distance, 2nd = force)
            print("split = ",split)
            if len(split) >= 2 and split[0] != "" and split[1] != "": #makes sure data is in proper formatting before processing (else pair: A)
                inches = split[0]
                pounds = split[1]
                
                try:
                    RecordForce.elapsed.insert(i, time.time() - start)# list of elapsed time
                    RecordForce.dis.insert(i, float(inches))# list of inches traveled
                    RecordForce.force.insert(i, float(pounds))# list of force traveled

                except:
                    errors.append('data append') # label 
                    eCode = 'e4'
                    errorCodes.append(eCode)  
                 #   popup("Arduino data error")
                  #  print(string[i])

                '''Scrollbars Options'''
                '''
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

                          '''
            else: # skips incoming data if not in right format (if pair: A
                errors.append('data skip (incorrect format)') # label 
                eCode = 'e5'
                errorCodes.append(eCode)
                '''
    except:
        if RecordForce.collect == True:
            errors.append('serial disconnect')
            eCode = 'e6'
            errorCodes.append(eCode)
        else:
            pass
            '''
        

        

        
''' Main '''
print("StemBerry is loading.....")
print("output: address = "+address)
print("script = "+script)
print("directory = "+directory)
print("ignoreserial = "+str(ignoreserial))
app = GUI() # INITIATES GUI TO START
app.title("StemBerry")
app.geometry("800x480+0+0")
app.aspect()
#app.geometry("700x700+0+0")
#fig = plt.figure()
#app.iconbitmap(s'/home/pi/Desktop/SOCEM Code')
#app.geometry("{0}x{1}+0+0".format(app.winfo_screenwidth()-3,app.winfo_screenheight()-3)) #full screen:
app.mainloop()
''' End '''
