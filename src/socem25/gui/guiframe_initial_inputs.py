import csv
from itertools import zip_longest
import tkinter as tk

#from socem25.gui.gui_main import SocemGuiMain
from socem25.core.pass_in import PassIn
from socem25.core.serial_connection import SerialConnection as SC
from socem25.gui.gui_main import RepeatPageButtons
from socem25.core.configuration import Config
import socem25.core.main_funcs
#Home page
class InitialInputs(tk.Frame,PassIn):
    def __init__(self, parent, controller): # automatically runs
        # Once the program launches, the InitialInput screen will be shown for the first time, prompting serial connection
        try:
            self.gui_record_force_object.ser = SC.serial_connect()
        except:
            self.gui_main_object.ignoreserial = True
            print("Serial not connected.")
        
        tk.Frame.__init__(self, parent)
        PassIn.__init__()
        
        ''' GUI design, non-frame '''
        pageButtons = RepeatPageButtons.showButtons(self, parent, controller)
        homeheader = tk.Label(self, text = "INITIAL INPUTS", font = ("arial", 17, "bold"), fg = "gray3", bg="ghost white")
        unit_label = tk.Label(self, text=str("Distance and height are in centimeters."), font = ("arial", 12, "italic"), fg = "red4", bg="ghost white")
        savePreTestInputs_button = tk.Button(self, text ="Save Initial Inputs", font = ("arial", 16, "bold"), height = 1, width = 20, fg = "ghost white", bg = "dodgerblue3", command=lambda:self.savePreTestInputs())
        variety_label = tk.Label(self, text = "Variety: ", font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white")
        varietyname_entryBox = tk.Entry(self, textvariable=self.gui_main_object.varietyname, font = ("arial", 14, "bold"), width="20", bg="white", fg="gray1")
        plotname_label = tk.Label(self, text = "Plot: ", font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white")
        plotname_entryBox = tk.Entry(self, textvariable=self.gui_main_object.plotname, font = ("arial", 14, "bold"), width="10", bg="white", fg="gray1")
        passfillednames_checkbox = tk.Checkbutton(self, text = "Use variety & plot names", variable = self.gui_main_object.passfillednames_checkbox, width=23, height=2, font = ("arial", 12), bg='ghost white')
        stemHeight_label = tk.Label(self, text = "Avg. Stem Height (cm):", font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white")
        stemHeight_entry = tk.Entry(self, textvariable=self.gui_main_object.stemheight, font = ("arial", 14, "bold"), width= 6, bg="white", fg="gray1")
        barHeight_label = tk.Label(self, text = "Bar Middle Height (cm):", font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white")
        barHeight_entry = tk.Entry(self, textvariable=self.gui_main_object.barmiddle, font = ("arial", 14, "bold"), width= 6, bg="white", fg="gray1")

        homeheader.place(x=275,y=0)
        unit_label.place(x=500,y=0)
        savePreTestInputs_button.place(x = 510, y = 340)
        variety_label.place(x=0,y=35)
        varietyname_entryBox.place(x = 80, y = 35)
        plotname_label.place(x=310,y=35)
        plotname_entryBox.place(x = 360, y = 35)
        passfillednames_checkbox.place(x = 540 , y = 25)
        stemHeight_label.place(x=0,y=240)
        stemHeight_entry.place(x = 220, y = 240)
        barHeight_label.place(x=0,y=280) 
        barHeight_entry.place(x = 220, y = 280)
        
        ''' Frame: Range'''
        range_frame = tk.LabelFrame(self, text='Side Hit Ranges',font = ("arial", 14, "bold"), width= 10, bg="white", fg="gray1")
        range_frame.place(x = 20, y = 80)
        startRange1Dis_label = tk.Label(range_frame, text = "Range 1 start (cm):", font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white").grid(row=2, column=0)
        startRange2Dis_label = tk.Label(range_frame, text = "Range 2 start (cm):", font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white").grid(row=1, column=0)
        startRange3Dis_label = tk.Label(range_frame, text = "Range 3 start (cm):", font = ("arial", 14, "bold"), fg = "gray3", bg="ghost white").grid(row=0, column=0)
        startRange1_entry = tk.Entry(range_frame, textvariable=self.gui_main_object.startRange1,font = ("arial", 14, "bold"), width= 4, bg="white", fg="gray1").grid(row=2, column=1)
        startRange2_entry = tk.Entry(range_frame, textvariable=self.gui_main_object.startRange2,font = ("arial", 14, "bold"), width= 4, bg="white", fg="gray1").grid(row=1, column=1)
        startRange3_entry = tk.Entry(range_frame, textvariable=self.gui_main_object.startRange3, font = ("arial", 14, "bold"), width= 4, bg="white", fg="gray1").grid(row=0, column=1)
        ''' end '''

        ''' Frame: Force Bar Quickset buttons'''
        barset_frame = tk.LabelFrame(self, text='Bar Bottom Quickset',font = ("arial", 14, "bold"), width= 10, bg="white", fg="gray1")
        barset_frame.place(x = 340, y = 230)
        #button that calculates optimized force bar height
        height70percent_button = tk.Button(barset_frame, text ="70%", font=("arial",14,"bold"), height=1, width=6, fg="ghost white", bg="red4",command=lambda:self.height70percent(self.gui_main_object.stemheight.get()))
        height80percent_button = tk.Button(barset_frame, text ="80%", font=("arial",14,"bold"), height=1, width=6, fg="ghost white", bg="red4",command=lambda:self.height80percent(self.gui_main_object.stemheight.get()))
        height90percent_button = tk.Button(barset_frame, text ="90%", font=("arial",14,"bold"), height=1, width=6, fg="ghost white", bg="red4",command=lambda:self.height90percent(self.gui_main_object.stemheight.get()))
        height70percent_button.grid(row=0, column=0)
        height80percent_button.grid(row=0, column=1)
        height90percent_button.grid(row=0, column=2)
        ''' end '''
        
        ''' Frame: PreCount Buttons '' # Hide, access via menu
        precount_frame = tk.LabelFrame(self, text='Count First',font = ("arial", 10, "bold"), width= 4, bg="white", fg="gray1")
        precount_frame.place(x = 650, y = 100)
        precount_button = tk.Button(precount_frame, text ="Don't", font=("arial",10,"bol;d"), height=1, width=10, fg="ghost white", bg="purple3",command=lambda:self.height70percent(self.gui_main_object.stemheight.get()))
        precount_button.grid(row=0, column=4)
        '' end '''
        
        self.bind("<<ShowFrame>>", self.on_show_frame_InitialInputs) # why is this really here

    def height70percent(self, stemheight):
        coeff = 0.7
        self.gui_main_object.barbottom.set(round(coeff*stemheight,3))
        self.gui_main_object.barmiddle.set(round(self.gui_main_object.barbottom.get()+Config.barradius,3))
        print("70%: stemheight",self.gui_main_object.stemheight.get(),"cm, barheight = ",self.gui_main_object.barmiddle.get(),"cm, barbottom = ",self.gui_main_object.barbottom.get(),"cm")
    def height80percent(self, stemheight):
        coeff = 0.8
        self.gui_main_object.barbottom.set(round(coeff*stemheight,3))
        self.gui_main_object.barmiddle.set(round(self.gui_main_object.barbottom.get()+Config.barradius,3))
        print("80%: stemheight",self.gui_main_object.stemheight.get(),"cm, barheight = ",self.gui_main_object.barmiddle.get(),"cm, barbottom = ",self.gui_main_object.barbottom.get(),"cm")
    def height90percent(self, stemheight):
        coeff = 0.9
        self.gui_main_object.barbottom.set(round(coeff*stemheight,3))
        self.gui_main_object.barmiddle.set(round(self.gui_main_object.barbottom.get()+Config.barradius,3))
        print("90%: stemheight",self.gui_main_object.stemheight.get(),"cm, barheight = ",self.gui_main_object.barmiddle.get(),"cm, barbottom = ",self.gui_main_object.barbottom.get(),"cm")
    
    def savePreTestInputs(self):
        self.gui_main_object.barbottom.set(round(self.gui_main_object.barmiddle.get()-Config.barradius,3)) # cm
        print(str(int(self.gui_main_object.barbottom.get()/self.gui_main_object.stemheight.get()*100)),"%: stemheight",self.gui_main_object.stemheight.get(),"cm, barheight = ",self.gui_main_object.barmiddle.get(),"cm, barbottom = ",self.gui_main_object.barbottom.get(),"cm")

        variety, plot, stemheight, barbottom, barmiddle, startRange1, startRange2, startRange3 = ['variety'], ['plot'], ['stemheight(cm)'], ['barbottom(cm)'], ['barmiddle(cm)'], ['startRange1(cm)'], ['startRange2(cm)'], ['startRange3(cm)']
        variety.append(self.gui_main_object.varietyname.get())
        plot.append(self.gui_main_object.plotname.get())
        stemheight.append(self.gui_main_object.stemheight.get())
        barbottom.append(self.gui_main_object.barbottom.get())
        barmiddle.append(self.gui_main_object.barmiddle.get())
        startRange1.append(self.gui_main_object.startRange1.get())
        startRange2.append(self.gui_main_object.startRange2.get())
        startRange3.append(self.gui_main_object.startRange3.get())
        
        socem25.core.main_funcs.update_filename_preTest()
        filename_preTest_csv = self.gui_main_object.address + '/' + self.gui_main_object.filename_preTest.get() + '.csv'

        if socem25.core.main_funcs.overwriteGuard(filename_preTest_csv) == True: # filename already exists, needs to be renamed
            socem25.core.main_funcs.rename(self.gui_main_object.filename_preTest.get()) # prompt user to rename file  
        ''' write CSV'''
        self.gui_main_object.data_preTest = [variety, plot, stemheight, barbottom, barmiddle, startRange1, startRange2, startRange3]
        columns_data_preTest = zip_longest(*self.gui_main_object.data_preTest)
        with open(filename_preTest_csv,'w',newline='') as f:
            writer = csv.writer(f)
            writer.writerows(columns_data_preTest)
        ''' end: write CSV '''
        print("filename_preTest_csv = "+filename_preTest_csv)
        
    def on_show_frame_InitialInputs(self, event):
        filler=1
        #print("show Initial Inputs screen")
