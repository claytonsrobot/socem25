import tkinter as tk

from gui.guiframe_final_inputs import FinalInputs
'''Classes, Tkinter GUI'''
# GUI overarching class
class SocemGUI(tk.Tk):

    @classmethod
    def pass_in_FinalInputs(cls,FinalInputs):
        cls.FinalInputs = FinalInputs
    def __init__(self, *args, **kwargs):# automatically runs
        self.nope = "nope"

    def run(self,*args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        SocemGUI.initializeVarsGUI()
        SocemGUI.refreshAll()
        
        container = tk.Frame(self)
        container.pack(side='top', fill='both',expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        # top menu configuration
        menubar = Menu(container)
        filemenu = Menu(menubar, tearoff=0)
        datamenu = Menu(menubar, tearoff=0)
        pagemenu = Menu(menubar, tearoff=0)
        
        filemenu.add_command(label='Serial Reconnect', command = lambda:serial_reconnect())
        filemenu.add_command(label='Choose Output Folder', command = lambda:popup_chooseFolder())
        filemenu.add_command(label='Errors', command = lambda:showErrors())
        filemenu.add_command(label='Save State', command = lambda:createBackupFile())
        filemenu.add_command(label='Restore State', command = lambda:restoreState())
        filemenu.add_command(label="Exit", command = lambda:close())
        pagemenu.add_command(label="Guide", command=lambda:SocemGUI.show_frame(Guide))
        pagemenu.add_command(label="Initial Inputs", command=lambda:SocemGUI.show_frame(InitialInputs))
        pagemenu.add_command(label="Record Force", command=lambda:SocemGUI.show_frame(RecordForce))
        pagemenu.add_command(label="Post Test Inputs", command=lambda:SocemGUI.show_frame(self.FinalInputs))
        pagemenu.add_command(label="Calibrate", command=lambda:SocemGUI.show_frame(Calibrate))
        pagemenu.add_command(label="Stem Count PreTest, Classic", command=lambda:SocemGUI.show_frame(StemCountClassic))
        datamenu.add_command(label="Data Feed Display, On", command = lambda:data_display(True))
        datamenu.add_command(label="Data Feed Display, Off", command = lambda:data_display(False))

        menubar.add_cascade(label='File', menu=filemenu)
        menubar.add_cascade(label="Pages", menu=pagemenu)
        menubar.add_cascade(label="Livestream Data Recording", menu=datamenu)
        
        tk.Tk.config(self, menu=menubar)                
        SocemGUI.frames = {}# empty dictionary

        for F in (InitialInputs, RecordForce, FinalInputs, Calibrate, Guide, ErrorReport, StemCountClassic):# must put all pages in here
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')
            frame.configure(background = 'ghost white')
        
        SocemGUI.show_frame(InitialInputs)
        
    def initializeVarsGUI():
        SocemGUI.filename_force = tk.StringVar()
        SocemGUI.filename_preTest = tk.StringVar()
        SocemGUI.filename_postTest = tk.StringVar()
        SocemGUI.filename_all = tk.StringVar()
        SocemGUI.varietyname = tk.StringVar()
        SocemGUI.plotname = tk.StringVar()
        SocemGUI.stemheight = tk.DoubleVar()
        SocemGUI.currentdirection = tk.StringVar()#
        SocemGUI.barmiddle = tk.DoubleVar() #
        SocemGUI.barbottom = tk.DoubleVar() #
        SocemGUI.passfillednames_checkbox = tk.IntVar() # revert
        SocemGUI.timestring = tk.StringVar()
        SocemGUI.startRange1, SocemGUI.startRange2, SocemGUI.startRange3 = tk.DoubleVar(),  tk.DoubleVar(),  tk.DoubleVar() # cm = tk.StringVar()
        SocemGUI.addressInput = tk.StringVar()
        
        SocemGUI.cell1Mass,SocemGUI.cell2Mass,SocemGUI.cell3Mass,SocemGUI.cell4Mass,SocemGUI.cell5Mass,SocemGUI.cell6Mass,SocemGUI.cell7Mass,SocemGUI.cell8Mass,SocemGUI.cell9Mass =  tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar()
        SocemGUI.cell1Count,SocemGUI.cell2Count,SocemGUI.cell3Count,SocemGUI.cell4Count,SocemGUI.cell5Count,SocemGUI.cell6Count,SocemGUI.cell7Count,SocemGUI.cell8Count,SocemGUI.cell9Count =  tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar()
        SocemGUI.cell1Diameter1,SocemGUI.cell2Diameter1,SocemGUI.cell3Diameter1,SocemGUI.cell4Diameter1,SocemGUI.cell5Diameter1,SocemGUI.cell6Diameter1,SocemGUI.cell7Diameter1,SocemGUI.cell8Diameter1,SocemGUI.cell9Diameter1 =  tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar()
        SocemGUI.cell1Diameter2,SocemGUI.cell2Diameter2,SocemGUI.cell3Diameter2,SocemGUI.cell4Diameter2,SocemGUI.cell5Diameter2,SocemGUI.cell6Diameter2,SocemGUI.cell7Diameter2,SocemGUI.cell8Diameter2,SocemGUI.cell9Diameter2 =  tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar()
        SocemGUI.cell1Diameter3,SocemGUI.cell2Diameter3,SocemGUI.cell3Diameter3,SocemGUI.cell4Diameter3,SocemGUI.cell5Diameter3,SocemGUI.cell6Diameter3,SocemGUI.cell7Diameter3,SocemGUI.cell8Diameter3,SocemGUI.cell9Diameter3 =  tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar()
        SocemGUI.cell1Diameter4,SocemGUI.cell2Diameter4,SocemGUI.cell3Diameter4,SocemGUI.cell4Diameter4,SocemGUI.cell5Diameter4,SocemGUI.cell6Diameter4,SocemGUI.cell7Diameter4,SocemGUI.cell8Diameter4,SocemGUI.cell9Diameter4 =  tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar(), tk.DoubleVar()

        ''' Non-tkinter GUI vars, initialize ''' # for nine cell assessment, save state
        # may as well keep everything here, for fun
        SocemGUI.errors = [] # for tracking errors
        SocemGUI.errorCodes = [] # for tracking errors
        SocemGUI.ignoreserial = ignoreserial
        SocemGUI.address = address

        SocemGUI.forcePushed = []
        SocemGUI.distanceTraveled = []
        SocemGUI.timeElapsed = []
        SocemGUI.travelvelocity = []
        SocemGUI.samplingrate = []

        SocemGUI.forcePushed_side1 = []
        SocemGUI.forcePushed_side2 = []
        SocemGUI.forcePushed_side3 = []
        SocemGUI.forcePushed_forward = []
        SocemGUI.distanceTraveled_side1 = []
        SocemGUI.distanceTraveled_side2 = []
        SocemGUI.distanceTraveled_side3 = []
        SocemGUI.distanceTraveled_forward = []
        SocemGUI.timeElapsed_side1 = []
        SocemGUI.timeElapsed_side2 = []
        SocemGUI.timeElapsed_side3 = []
        SocemGUI.timeElapsed_forward =  []
        SocemGUI.peaks_force_side1 = []
        SocemGUI.peaks_force_side2 = []        
        SocemGUI.peaks_force_side3 = []
        SocemGUI.peaks_force_forward = []
        SocemGUI.peaks_distance_side1 = []
        SocemGUI.peaks_distance_side2 = []        
        SocemGUI.peaks_distance_side3 = []
        SocemGUI.peaks_distance_forward = []
        SocemGUI.peaks_time_side1 = []
        SocemGUI.peaks_time_side2 = []        
        SocemGUI.peaks_time_side3 = []
        SocemGUI.peaks_time_forward = []

        SocemGUI.peaks_force = []
        SocemGUI.peaks_distance = []
        SocemGUI.peaks_time = []

        peakclick.peaks_force = []
        peakclick.peaks_distance = []
        peakclick.peaks_time = []

        SocemGUI.stemcounts = []

        SocemGUI.peak_force_cell1, SocemGUI.peak_force_cell2, SocemGUI.peak_force_cell3, SocemGUI.peak_force_cell4, SocemGUI.peak_force_cell5, SocemGUI.peak_force_cell6, SocemGUI.peak_force_cell7, SocemGUI.peak_force_cell8, SocemGUI.peak_force_cell9 = 0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
        SocemGUI.peak_distance_cell1, SocemGUI.peak_distance_cell2, SocemGUI.peak_distance_cell3, SocemGUI.peak_distance_cell4, SocemGUI.peak_distance_cell5, SocemGUI.peak_distance_cell6, SocemGUI.peak_distance_cell7, SocemGUI.peak_distance_cell8, SocemGUI.peak_distance_cell9 = 0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
        SocemGUI.peak_time_cell1, SocemGUI.peak_time_cell2, SocemGUI.peak_time_cell3, SocemGUI.peak_time_cell4, SocemGUI.peak_time_cell5, SocemGUI.peak_time_cell6, SocemGUI.peak_time_cell7, SocemGUI.peak_time_cell8, SocemGUI.peak_time_cell9 = 0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0

        SocemGUI.data_preTest,SocemGUI.data_recordForce,SocemGUI.data_postTest,SocemGUI.data_peaks,SocemGUI.data_EI = [],[],[],[],[]
        
    def refreshAll(): #clear_all(self)?
        
    
        SocemGUI.filename_force.set("")
        SocemGUI.filename_preTest.set("")
        SocemGUI.filename_postTest.set("")
        SocemGUI.filename_all.set("")
        SocemGUI.varietyname.set("")
        SocemGUI.plotname.set("")
        SocemGUI.startRange1.set(50)
        SocemGUI.startRange2.set(150) 
        SocemGUI.startRange3.set(250) # centimeters
        SocemGUI.stemheight.set(default_stemheight) # cm
        SocemGUI.barbottom.set(round(SocemGUI.stemheight.get()*initial_barbottomOverStemheight_coeff,3)) # cm
        SocemGUI.barmiddle.set(round(SocemGUI.barbottom.get()+barradius,3)) # cm
        SocemGUI.passfillednames_checkbox.set(1)
        SocemGUI.timestring.set(time.strftime("%H%M"))
        SocemGUI.currentdirection.set("")
        SocemGUI.addressInput.set("")
        
        ''' Set post test variables for mass, count, and diameter'''
        SocemGUI.cell1Mass.set(0),SocemGUI.cell2Mass.set(0),SocemGUI.cell3Mass.set(0),SocemGUI.cell4Mass.set(0),SocemGUI.cell5Mass.set(0),SocemGUI.cell6Mass.set(0),SocemGUI.cell7Mass.set(0),SocemGUI.cell8Mass.set(0),SocemGUI.cell9Mass.set(0)
        SocemGUI.cell1Count.set(0),SocemGUI.cell2Count.set(0),SocemGUI.cell3Count.set(0),SocemGUI.cell4Count.set(0),SocemGUI.cell5Count.set(0),SocemGUI.cell6Count.set(0),SocemGUI.cell7Count.set(0),SocemGUI.cell8Count.set(0),SocemGUI.cell9Count.set(0)
        SocemGUI.cell1Diameter1.set(0),SocemGUI.cell2Diameter1.set(0),SocemGUI.cell3Diameter1.set(0),SocemGUI.cell4Diameter1.set(0),SocemGUI.cell5Diameter1.set(0),SocemGUI.cell6Diameter1.set(0),SocemGUI.cell7Diameter1.set(0),SocemGUI.cell8Diameter1.set(0),SocemGUI.cell9Diameter1.set(0)
        SocemGUI.cell1Diameter2.set(0),SocemGUI.cell2Diameter2.set(0),SocemGUI.cell3Diameter2.set(0),SocemGUI.cell4Diameter2.set(0),SocemGUI.cell5Diameter2.set(0),SocemGUI.cell6Diameter2.set(0),SocemGUI.cell7Diameter2.set(0),SocemGUI.cell8Diameter2.set(0),SocemGUI.cell9Diameter2.set(0)
        SocemGUI.cell1Diameter3.set(0),SocemGUI.cell2Diameter3.set(0),SocemGUI.cell3Diameter3.set(0),SocemGUI.cell4Diameter3.set(0),SocemGUI.cell5Diameter3.set(0),SocemGUI.cell6Diameter3.set(0),SocemGUI.cell7Diameter3.set(0),SocemGUI.cell8Diameter3.set(0),SocemGUI.cell9Diameter3.set(0)
        SocemGUI.cell1Diameter4.set(0),SocemGUI.cell2Diameter4.set(0),SocemGUI.cell3Diameter4.set(0),SocemGUI.cell4Diameter4.set(0),SocemGUI.cell5Diameter4.set(0),SocemGUI.cell6Diameter4.set(0),SocemGUI.cell7Diameter4.set(0),SocemGUI.cell8Diameter4.set(0),SocemGUI.cell9Diameter4.set(0)

        if autopopulatestemcount == True:
            SocemGUI.cell1Count.set(defaultstemcount),SocemGUI.cell2Count.set(defaultstemcount),SocemGUI.cell3Count.set(defaultstemcount),SocemGUI.cell4Count.set(defaultstemcount),SocemGUI.cell5Count.set(defaultstemcount),SocemGUI.cell6Count.set(defaultstemcount),SocemGUI.cell7Count.set(defaultstemcount),SocemGUI.cell8Count.set(defaultstemcount),SocemGUI.cell9Count.set(defaultstemcount)
        ''' end '''
        
        ''' Non-tkinter GUI vars, initialize ''' # for nine cell assessment, save state
        # may as well keep everything here, for fun
        SocemGUI.errors = [] # for tracking errors
        SocemGUI.errorCodes = [] # for tracking errors

        SocemGUI.forcePushed = []
        SocemGUI.distanceTraveled = []
        SocemGUI.timeElapsed = []

        SocemGUI.forcePushed_side1 = []
        SocemGUI.forcePushed_side2 = []
        SocemGUI.forcePushed_side3 = []
        SocemGUI.forcePushed_forward = []
        SocemGUI.distanceTraveled_side1 = []
        SocemGUI.distanceTraveled_side2 = []
        SocemGUI.distanceTraveled_side3 = []
        SocemGUI.distanceTraveled_forward = []
        SocemGUI.timeElapsed_side1 = []
        SocemGUI.timeElapsed_side2 = []
        SocemGUI.timeElapsed_side3 = []
        SocemGUI.timeElapsed_forward =  []
        SocemGUI.peaks_force_side1 = []
        SocemGUI.peaks_force_side2 = []        
        SocemGUI.peaks_force_side3 = []
        SocemGUI.peaks_force_forward = []
        SocemGUI.peaks_distance_side1 = []
        SocemGUI.peaks_distance_side2 = []        
        SocemGUI.peaks_distance_side3 = []
        SocemGUI.peaks_distance_forward = []
        SocemGUI.peaks_time_side1 = []
        SocemGUI.peaks_time_side2 = []        
        SocemGUI.peaks_time_side3 = []

        SocemGUI.peaks_force = []
        SocemGUI.peaks_distance = []
        SocemGUI.peaks_time = []

        SocemGUI.stemcounts = []

        SocemGUI.peak_force_cell1, SocemGUI.peak_force_cell2, SocemGUI.peak_force_cell3, SocemGUI.peak_force_cell4, SocemGUI.peak_force_cell5, SocemGUI.peak_force_cell6, SocemGUI.peak_force_cell7, SocemGUI.peak_force_cell8, SocemGUI.peak_force_cell9 = 0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
        SocemGUI.peak_distance_cell1, SocemGUI.peak_distance_cell2, SocemGUI.peak_distance_cell3, SocemGUI.peak_distance_cell4, SocemGUI.peak_distance_cell5, SocemGUI.peak_distance_cell6, SocemGUI.peak_distance_cell7, SocemGUI.peak_distance_cell8, SocemGUI.peak_distance_cell9 = 0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
        SocemGUI.peak_time_cell1, SocemGUI.peak_time_cell2, SocemGUI.peak_time_cell3, SocemGUI.peak_time_cell4, SocemGUI.peak_time_cell5, SocemGUI.peak_time_cell6, SocemGUI.peak_time_cell7, SocemGUI.peak_time_cell8, SocemGUI.peak_time_cell9 = 0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
        
        SocemGUI.peak_EI_fullcontact_cell1, SocemGUI.peak_EI_fullcontact_cell2, SocemGUI.peak_EI_fullcontact_cell3, SocemGUI.peak_EI_fullcontact_cell4, SocemGUI.peak_EI_fullcontact_cell5, SocemGUI.peak_EI_fullcontact_cell6, SocemGUI.peak_EI_fullcontact_cell7, SocemGUI.peak_EI_fullcontact_cell8, SocemGUI.peak_EI_fullcontact_cell9 = [],[],[],[],[],[],[],[],[]
        SocemGUI.peak_EI_intermediatecontact_cell1, SocemGUI.peak_EI_intermediatecontact_cell2, SocemGUI.peak_EI_intermediatecontact_cell3, SocemGUI.peak_EI_intermediatecontact_cell4, SocemGUI.peak_EI_intermediatecontact_cell5, SocemGUI.peak_EI_intermediatecontact_cell6, SocemGUI.peak_EI_intermediatecontact_cell7, SocemGUI.peak_EI_intermediatecontact_cell8, SocemGUI.peak_EI_intermediatecontact_cell9 = [],[],[],[],[],[],[],[],[]
        SocemGUI.peak_EI_nocontact_cell1, SocemGUI.peak_EI_nocontact_cell2, SocemGUI.peak_EI_nocontact_cell3, SocemGUI.peak_EI_nocontact_cell4, SocemGUI.peak_EI_nocontact_cell5, SocemGUI.peak_EI_nocontact_cell6, SocemGUI.peak_EI_nocontact_cell7, SocemGUI.peak_EI_nocontact_cell8, SocemGUI.peak_EI_nocontact_cell9 = [],[],[],[],[],[],[],[],[]

        SocemGUI.peaks_time_forward = []
        SocemGUI.EI_fullcontact = [] 
        SocemGUI.EI_intermediatecontact = []
        SocemGUI.EI_nocontact = []
        SocemGUI.AvgEI_intermediatecontact = []

        SocemGUI.data_preTest,SocemGUI.data_recordForce,SocemGUI.data_postTest,SocemGUI.data_peaks,SocemGUI.data_EI = [],[],[],[],[]
    
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
        guide_button = tk.Button(self, text = "Guide", font = ("arial", 14, "bold"), height = 2, width = 8, fg = "ghost white", bg = "gray2",command=lambda:SocemGUI.show_frame(Guide))
        initialInputs_button = tk.Button(self, text = "Initial\nInputs", font = ("arial", 14, "bold"), height = 2, width = 8, fg = "ghost white", bg = "gray2",command=lambda:SocemGUI.show_frame(InitialInputs))
        recordForce_button = tk.Button(self, text = "Record\nForce", font = ("arial", 14, "bold"), height = 2, width = 8, fg = "ghost white", bg = "gray2",command=lambda:SocemGUI.show_frame(RecordForce))
        postInputs_button = tk.Button(self, text = "Post Test\nInputs", font = ("arial", 14, "bold"), height = 2, width = 8, fg = "ghost white", bg = "gray2",command=lambda:SocemGUI.show_frame(FinalInputs))

        guide_button.place(x = 0, y = 340)
        initialInputs_button.place(x = 375/3*1, y = 340)
        recordForce_button.place(x = 375/3*2, y = 340)
        postInputs_button.place(x = 375/3*3, y = 340)
        #'''
