import tkinter as tk
import time

#from gui.guiframe_final_inputs import gui_final_inputs_object replaced by cls.pass_in_gui_final_inputs_object()
from src.serial_connection import SerialConnection as SC #import serial_reconnect
from src import main_funcs
from src.userclicks import PeakClick 
from src.configuration import Config
from src.pass_in import PassIn
'''Classes, Tkinter GUI'''
# GUI overarching class
class SocemGUI(tk.Tk,PassIn):

    @classmethod
    def pass_in_gui_final_inputs_object(cls,gui_final_inputs_object):
        cls.gui_final_inputs_object = gui_final_inputs_object
    
    @classmethod
    def pass_in_gui_peak_clicks_object(cls,gui_peak_clicks_object):
        cls.gui_peak_clicks_object = gui_peak_clicks_object

    @classmethod
    def pass_in_gui_record_force_object(cls,gui_record_force_object):
        cls.gui_record_force_object = gui_record_force_object

    @classmethod
    def pass_in_gui_initial_inputs_object(cls,gui_initial_inputs_object):
        cls.gui_initial_inputs_object = gui_initial_inputs_object
    
    @classmethod
    def pass_in_gui_calibrate_object(cls,gui_calibrate_object):
        cls.gui_calibrate_object = gui_calibrate_object

    @classmethod
    def pass_in_gui_stem_count_classic_object(cls,gui_stem_count_classic_object):
        cls.gui_stem_count_classic_object = gui_stem_count_classic_object

    @classmethod
    def pass_in_gui_guide_object(cls,gui_guide_object):
        cls.gui_guide_object = gui_guide_object

    def __init__(self, *args, **kwargs):# automatically runs
        self.nope = "nope"
    
    def pass_from_gui_main_object(self,other_class):
        other_class.gui_main_object = self

    def run(self,*args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.initialize_tk_vars_gui_main()
        self.refresh_tk_vars_gui_main()
        
        container = tk.Frame(self)
        container.pack(side='top', fill='both',expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        # top menu configuration
        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar, tearoff=0)
        datamenu = tk.Menu(menubar, tearoff=0)
        pagemenu = tk.Menu(menubar, tearoff=0)
        
        filemenu.add_command(label='Serial Reconnect', command = lambda:SC.serial_reconnect())
        filemenu.add_command(label='Choose Output Folder', command = lambda:main_funcs.popup_chooseFolder())
        filemenu.add_command(label='Errors', command = lambda:main_funcs.showErrors())
        filemenu.add_command(label='Save State', command = lambda:main_funcs.createBackupFile())
        filemenu.add_command(label='Restore State', command = lambda:main_funcs.restoreState())
        filemenu.add_command(label="Exit", command = lambda:main_funcs.close())
        pagemenu.add_command(label="Guide", command=lambda:self.show_frame(self.gui_guide_object))
        pagemenu.add_command(label="Initial Inputs", command=lambda:self.show_frame(self.gui_initial_inputs_object))
        pagemenu.add_command(label="Record Force", command=lambda:self.show_frame(self.gui_record_force_object))
        pagemenu.add_command(label="Post Test Inputs", command=lambda:self.show_frame(self.gui_final_inputs_object))
        pagemenu.add_command(label="Calibrate", command=lambda:self.show_frame(self.gui_calibrate_object))
        pagemenu.add_command(label="Stem Count PreTest, Classic", command=lambda:self.show_frame(self.gui_stem_count_classic_object))
        datamenu.add_command(label="Data Feed Display, On", command = lambda:main_funcs.data_display(True))
        datamenu.add_command(label="Data Feed Display, Off", command = lambda:main_funcs.data_display(False))

        menubar.add_cascade(label='File', menu=filemenu)
        menubar.add_cascade(label="Pages", menu=pagemenu)
        menubar.add_cascade(label="Livestream Data Recording", menu=datamenu)
        
        tk.Tk.config(self, menu=menubar)                
        self.frames = {}# empty dictionary

        for F in (self.gui_initial_inputs_object, self.gui_record_force_object, self.gui_final_inputs_object, self.gui_calibrate_object, self.gui_guide_object, self.gui_error_report_object, self.gui_stem_count_classic_object):# must put all pages in here
            frame = F(container, self)
            print(f"frame = {frame}")
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')
            frame.configure(background = 'ghost white')
        
        self.show_frame(self.gui_initial_inputs_object)
        
    def initialize_tk_vars_gui_main(self):
        self.filename_force = tk.StringVar()
        self.filename_preTest = tk.StringVar()
        self.filename_postTest = tk.StringVar()
        self.filename_all = tk.StringVar()
        self.varietyname = tk.StringVar()
        self.plotname = tk.StringVar()
        self.stemheight = tk.DoubleVar()
        self.currentdirection = tk.StringVar()#
        self.barmiddle = tk.DoubleVar() #
        self.barbottom = tk.DoubleVar() #
        self.passfillednames_checkbox = tk.IntVar() # revert
        self.timestring = tk.StringVar()
        self.startRange1, self.startRange2, self.startRange3 = tk.DoubleVar(),  tk.DoubleVar(),  tk.DoubleVar() # cm = tk.StringVar()
        self.addressInput = tk.StringVar()
        
        self.cell1Mass,self.cell2Mass,self.cell3Mass,self.cell4Mass,self.cell5Mass,self.cell6Mass,self.cell7Mass,self.cell8Mass,self.cell9Mass =  tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar()
        self.cell1Count,self.cell2Count,self.cell3Count,self.cell4Count,self.cell5Count,self.cell6Count,self.cell7Count,self.cell8Count,self.cell9Count =  tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar()
        self.cell1Diameter1,self.cell2Diameter1,self.cell3Diameter1,self.cell4Diameter1,self.cell5Diameter1,self.cell6Diameter1,self.cell7Diameter1,self.cell8Diameter1,self.cell9Diameter1 =  tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar()
        self.cell1Diameter2,self.cell2Diameter2,self.cell3Diameter2,self.cell4Diameter2,self.cell5Diameter2,self.cell6Diameter2,self.cell7Diameter2,self.cell8Diameter2,self.cell9Diameter2 =  tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar()
        self.cell1Diameter3,self.cell2Diameter3,self.cell3Diameter3,self.cell4Diameter3,self.cell5Diameter3,self.cell6Diameter3,self.cell7Diameter3,self.cell8Diameter3,self.cell9Diameter3 =  tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar()
        self.cell1Diameter4,self.cell2Diameter4,self.cell3Diameter4,self.cell4Diameter4,self.cell5Diameter4,self.cell6Diameter4,self.cell7Diameter4,self.cell8Diameter4,self.cell9Diameter4 =  tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar()
    def initialize_nine_cell_vars(self):
        '''For generic and nine-cell assessment GUI vars, initialize ''' 
        # for nine cell assessment, save state
        self.errors = [] # for tracking errors
        self.errorCodes = [] # for tracking errors
        self.ignoreserial = False #ignoreserial
        self.address = ""
        #self.address = Directory.get_ # modularize with Address class

        self.forcePushed = []
        self.distanceTraveled = []
        self.timeElapsed = []
        self.travelvelocity = []
        self.samplingrate = []

        self.forcePushed_side1 = []
        self.forcePushed_side2 = []
        self.forcePushed_side3 = []
        self.forcePushed_forward = []
        self.distanceTraveled_side1 = []
        self.distanceTraveled_side2 = []
        self.distanceTraveled_side3 = []
        self.distanceTraveled_forward = []
        self.timeElapsed_side1 = []
        self.timeElapsed_side2 = []
        self.timeElapsed_side3 = []
        self.timeElapsed_forward =  []
        self.peaks_force_side1 = []
        self.peaks_force_side2 = []        
        self.peaks_force_side3 = []
        self.peaks_force_forward = []
        self.peaks_distance_side1 = []
        self.peaks_distance_side2 = []        
        self.peaks_distance_side3 = []
        self.peaks_distance_forward = []
        self.peaks_time_side1 = []
        self.peaks_time_side2 = []        
        self.peaks_time_side3 = []
        self.peaks_time_forward = []

        self.peaks_force = []
        self.peaks_distance = []
        self.peaks_time = []

        PeakClick.set_peaks_force(self.peaks_force)
        PeakClick.set_peaks_distance(self.peaks_distance)
        PeakClick.set_peaks_time(self.peaks_time)

        self.peak_force_cell1, self.peak_force_cell2, self.peak_force_cell3, self.peak_force_cell4, self.peak_force_cell5, self.peak_force_cell6, self.peak_force_cell7, self.peak_force_cell8, self.peak_force_cell9 = 0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
        self.peak_distance_cell1, self.peak_distance_cell2, self.peak_distance_cell3, self.peak_distance_cell4, self.peak_distance_cell5, self.peak_distance_cell6, self.peak_distance_cell7, self.peak_distance_cell8, self.peak_distance_cell9 = 0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
        self.peak_time_cell1, self.peak_time_cell2, self.peak_time_cell3, self.peak_time_cell4, self.peak_time_cell5, self.peak_time_cell6, self.peak_time_cell7, self.peak_time_cell8, self.peak_time_cell9 = 0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0

        self.data_preTest,self.data_recordForce,self.data_postTest,self.data_peaks,self.data_EI = [],[],[],[],[]
        
        self.peak_EI_fullcontact_cell1, self.peak_EI_fullcontact_cell2, self.peak_EI_fullcontact_cell3, self.peak_EI_fullcontact_cell4, self.peak_EI_fullcontact_cell5, self.peak_EI_fullcontact_cell6, self.peak_EI_fullcontact_cell7, self.peak_EI_fullcontact_cell8, self.peak_EI_fullcontact_cell9 = [],[],[],[],[],[],[],[],[]
        self.peak_EI_intermediatecontact_cell1, self.peak_EI_intermediatecontact_cell2, self.peak_EI_intermediatecontact_cell3, self.peak_EI_intermediatecontact_cell4, self.peak_EI_intermediatecontact_cell5, self.peak_EI_intermediatecontact_cell6, self.peak_EI_intermediatecontact_cell7, self.peak_EI_intermediatecontact_cell8, self.peak_EI_intermediatecontact_cell9 = [],[],[],[],[],[],[],[],[]
        self.peak_EI_nocontact_cell1, self.peak_EI_nocontact_cell2, self.peak_EI_nocontact_cell3, self.peak_EI_nocontact_cell4, self.peak_EI_nocontact_cell5, self.peak_EI_nocontact_cell6, self.peak_EI_nocontact_cell7, self.peak_EI_nocontact_cell8, self.peak_EI_nocontact_cell9 = [],[],[],[],[],[],[],[],[]

        self.peaks_time_forward = []
        self.EI_fullcontact = [] 
        self.EI_intermediatecontact = []
        self.EI_nocontact = []
        self.AvgEI_intermediatecontact = []

    def refresh_tk_vars_gui_main(self): #clear_all(self)?
    
        self.filename_force.set("")
        self.filename_preTest.set("")
        self.filename_postTest.set("")
        self.filename_all.set("")
        self.varietyname.set("")
        self.plotname.set("")
        self.startRange1.set(50)
        self.startRange2.set(150) 
        self.startRange3.set(250) # centimeters
        self.stemheight.set(Config.default_stemheight) # cm
        self.barbottom.set(round(self.stemheight.get()*Config.initial_barbottomOverStemheight_coeff,3)) # cm
        self.barmiddle.set(round(self.barbottom.get()+Config.barradius,3)) # cm
        self.passfillednames_checkbox.set(1)
        self.timestring.set(time.strftime("%H%M"))
        self.currentdirection.set("")
        self.addressInput.set("")
        
        ''' Set post test variables for mass, count, and diameter'''
        self.cell1Mass.set(0),self.cell2Mass.set(0),self.cell3Mass.set(0),self.cell4Mass.set(0),self.cell5Mass.set(0),self.cell6Mass.set(0),self.cell7Mass.set(0),self.cell8Mass.set(0),self.cell9Mass.set(0)
        self.cell1Count.set(0),self.cell2Count.set(0),self.cell3Count.set(0),self.cell4Count.set(0),self.cell5Count.set(0),self.cell6Count.set(0),self.cell7Count.set(0),self.cell8Count.set(0),self.cell9Count.set(0)
        self.cell1Diameter1.set(0),self.cell2Diameter1.set(0),self.cell3Diameter1.set(0),self.cell4Diameter1.set(0),self.cell5Diameter1.set(0),self.cell6Diameter1.set(0),self.cell7Diameter1.set(0),self.cell8Diameter1.set(0),self.cell9Diameter1.set(0)
        self.cell1Diameter2.set(0),self.cell2Diameter2.set(0),self.cell3Diameter2.set(0),self.cell4Diameter2.set(0),self.cell5Diameter2.set(0),self.cell6Diameter2.set(0),self.cell7Diameter2.set(0),self.cell8Diameter2.set(0),self.cell9Diameter2.set(0)
        self.cell1Diameter3.set(0),self.cell2Diameter3.set(0),self.cell3Diameter3.set(0),self.cell4Diameter3.set(0),self.cell5Diameter3.set(0),self.cell6Diameter3.set(0),self.cell7Diameter3.set(0),self.cell8Diameter3.set(0),self.cell9Diameter3.set(0)
        self.cell1Diameter4.set(0),self.cell2Diameter4.set(0),self.cell3Diameter4.set(0),self.cell4Diameter4.set(0),self.cell5Diameter4.set(0),self.cell6Diameter4.set(0),self.cell7Diameter4.set(0),self.cell8Diameter4.set(0),self.cell9Diameter4.set(0)

        if Config.autopopulatestemcount == True:
            self.cell1Count.set(Config.defaultstemcount),self.cell2Count.set(Config.defaultstemcount),self.cell3Count.set(Config.defaultstemcount),self.cell4Count.set(Config.defaultstemcount),self.cell5Count.set(Config.defaultstemcount),self.cell6Count.set(Config.defaultstemcount),self.cell7Count.set(Config.defaultstemcount),self.cell8Count.set(Config.defaultstemcount),self.cell9Count.set(Config.defaultstemcount)
        ''' end '''

    def show_frame(cont):
        frame = SocemGUI.frames[cont]
        frame.tkraise()
        frame.event_generate("<<ShowFrame>>") # event

# buttons that are the same for each page
#'''
class repeatPageButtons:
    def __init__(self, parent, controller): # automatically runs
        filler=1
    def showButtons(self, parent, controller):
        guide_button = tk.Button(self, text = "Guide", font = ("arial", 14, "bold"), height = 2, width = 8, fg = "ghost white", bg = "gray2",command=lambda:self.show_frame(self.gui_guide_object))
        initialInputs_button = tk.Button(self, text = "Initial\nInputs", font = ("arial", 14, "bold"), height = 2, width = 8, fg = "ghost white", bg = "gray2",command=lambda:self.show_frame(self.gui_initial_inputs_object))
        recordForce_button = tk.Button(self, text = "Record\nForce", font = ("arial", 14, "bold"), height = 2, width = 8, fg = "ghost white", bg = "gray2",command=lambda:self.show_frame(self.gui_record_force_object))
        postInputs_button = tk.Button(self, text = "Post Test\nInputs", font = ("arial", 14, "bold"), height = 2, width = 8, fg = "ghost white", bg = "gray2",command=lambda:self.show_frame(self.gui_final_inputs_object))

        guide_button.place(x = 0, y = 340)
        initialInputs_button.place(x = 375/3*1, y = 340)
        recordForce_button.place(x = 375/3*2, y = 340)
        postInputs_button.place(x = 375/3*3, y = 340)
        #'''
