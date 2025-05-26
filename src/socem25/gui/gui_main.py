import tkinter as tk
import time

#from socem25.gui.guiframe_final_inputs import gui_final_inputs_object replaced by cls.pass_in_gui_final_inputs_object()
from socem25.core.serial_connection import SerialConnection as SC #import serial_reconnect
import socem25.core.main_funcs
from socem25.core.userclicks import PeakClick 
from socem25.core.pass_in import PassIn
'''Classes, Tkinter GUI'''
# GUI overarching class

class SocemGuiMain(PassIn, tk.Frame):
    def __init__(self, parent, controller):
        # Call PassIn's constructor with parent
        PassIn.__init__(self, parent)
        # Initialize tk.Frame
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.parent = parent
        self.render(controller)

    def this_is_done_in__main__(self,*args, **kwargs):
        tk.Tk.__init__(self,*args, **kwargs)
    def render(self,controller,config):
        
        self.initialize_tk_vars_gui_main(controller)
        
        # Frame setup code (menus, containers, etc.)
        container = tk.Frame(self)
        container.pack(side='top', fill='both',expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
         # Set the container to the frame's container (needed for the menu setup)
        self.container = container
              
        self.frames = {}# empty dictionary
        for F in (self.gui_initial_inputs_object, self.gui_record_force_object, self.gui_final_inputs_object, self.gui_calibrate_object, self.gui_guide_object, self.gui_error_report_object, self.gui_stem_count_classic_object):# must put all pages in here
            frame = F(container, self)
            print(f"frame = {frame}")
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')
            frame.configure(background = 'ghost white')
        
        self.show_frame(self.gui_initial_inputs_object)
        self.configure_top_menu()

    def show_frame(self,cont):
        frame = self.frames[cont]
        frame.tkraise()
        frame.event_generate("<<ShowFrame>>") # event

    def configure_top_menu(self):
        # top menu configuration
        menubar = tk.Menu(self.container)
        filemenu = tk.Menu(menubar, tearoff=0)
        datamenu = tk.Menu(menubar, tearoff=0)
        pagemenu = tk.Menu(menubar, tearoff=0)
        
        filemenu.add_command(label='Serial Reconnect', command = lambda:SC.serial_reconnect())
        filemenu.add_command(label='Choose Output Folder', command = lambda:socem25.core.main_funcs.popup_chooseFolder())
        filemenu.add_command(label='Errors', command = lambda:socem25.core.main_funcs.showErrors())
        filemenu.add_command(label='Save State', command = lambda:socem25.core.main_funcs.createBackupFile())
        filemenu.add_command(label='Restore State', command = lambda:socem25.core.main_funcs.restoreState())
        filemenu.add_command(label="Exit", command = lambda:socem25.core.main_funcs.close())
        pagemenu.add_command(label="Guide", command=lambda:self.show_frame(self.gui_guide_object))
        pagemenu.add_command(label="Initial Inputs", command=lambda:self.show_frame(self.gui_initial_inputs_object))
        pagemenu.add_command(label="Record Force", command=lambda:self.show_frame(self.gui_record_force_object))
        pagemenu.add_command(label="Post Test Inputs", command=lambda:self.show_frame(self.gui_final_inputs_object))
        pagemenu.add_command(label="Calibrate", command=lambda:self.show_frame(self.gui_calibrate_object))
        pagemenu.add_command(label="Stem Count PreTest, Classic", command=lambda:self.show_frame(self.gui_stem_count_classic_object))
        datamenu.add_command(label="Data Feed Display, On", command = lambda:socem25.core.main_funcs.data_display(True))
        datamenu.add_command(label="Data Feed Display, Off", command = lambda:socem25.core.main_funcs.data_display(False))

        menubar.add_cascade(label='File', menu=filemenu)
        menubar.add_cascade(label="Pages", menu=pagemenu)
        menubar.add_cascade(label="Livestream Data Recording", menu=datamenu)
        
        tk.Tk.config(self, menu=menubar)  
        
    def initialize_tk_vars_gui_main(self,controller):

        tk_vars_gui_main = {
            "filename_force": tk.StringVar(),
            "filename_preTest": tk.StringVar(),
            "filename_postTest": tk.StringVar(),
            "filename_all": tk.StringVar(),
            "varietyname": tk.StringVar(),
            "plotname": tk.StringVar(),
            "stemheight": tk.DoubleVar(),
            "currentdirection": tk.StringVar(),
            "barmiddle": tk.DoubleVar(),
            "barbottom": tk.DoubleVar(),
            "passfillednames_checkbox": tk.IntVar(),
            "timestring": tk.StringVar(),
            "startRange1": tk.DoubleVar(),
            "startRange2": tk.DoubleVar(),
            "startRange3": tk.DoubleVar(),
            "addressInput": tk.StringVar()
        }
        controller.shared_data["main_frame"].update(tk_vars_gui_main)
        
        controller.shared_data["main_frame"]["filename_force"] = tk.StringVar()
        controller.shared_data["main_frame"]["filename_preTest"] = tk.StringVar()
        controller.shared_data["main_frame"]["filename_postTest"] = tk.StringVar()
        controller.shared_data["main_frame"]["filename_all"] = tk.StringVar()
        controller.shared_data["main_frame"]["varietyname"] = tk.StringVar()
        controller.shared_data["main_frame"]["plotname"] = tk.StringVar()
        controller.shared_data["main_frame"]["stemheight"] = tk.DoubleVar()
        controller.shared_data["main_frame"]["currentdirection"] = tk.StringVar()#
        controller.shared_data["main_frame"]["barmiddle"] = tk.DoubleVar() #
        controller.shared_data["main_frame"]["barbottom"] = tk.DoubleVar() #
        controller.shared_data["main_frame"]["passfillednames_checkbox"] = tk.IntVar() # revert
        controller.shared_data["main_frame"]["timestring"] = tk.StringVar()
        controller.shared_data["main_frame"]["startRange1"], controller.shared_data["main_frame"]["startRange2"], controller.shared_data["main_frame"]["startRange3"] = tk.DoubleVar(),  tk.DoubleVar(),  tk.DoubleVar() # cm = tk.StringVar()
        controller.shared_data["main_frame"]["addressInput"] = tk.StringVar()
        
        # Initialize cellular attributes     
        cellular_data = {
            f"cell{i}": {
                "mass": tk.DoubleVar(value=0.0),
                "count": tk.DoubleVar(value=0.0),
                "diameter1": tk.DoubleVar(value=0.0),
                "diameter2": tk.DoubleVar(value=0.0),
                "diameter3": tk.DoubleVar(value=0.0),
                "diameter4": tk.DoubleVar(value=0.0),
                }
                for i in range(1, 10)
            }
        controller.shared_data["main_frame"].update(cellular_data)

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

    def refresh_tk_vars_gui_main(self,controller): #clear_all(self)?
        self.initialize_tk_vars_gui_main()
    
        controller.shared_data["main_frame"]["filename_force"].set("")
        controller.shared_data["main_frame"]["filename_preTest"].set("")
        controller.shared_data["main_frame"]["filename_postTest"].set("")
        controller.shared_data["main_frame"]["filename_all"].set("")
        controller.shared_data["main_frame"]["varietyname"].set("")
        controller.shared_data["main_frame"]["plotname"].set("")
        controller.shared_data["main_frame"]["startRange1"].set(50)
        controller.shared_data["main_frame"]["startRange2"].set(150) 
        controller.shared_data["main_frame"]["startRange3"].set(250) # centimeters
        controller.shared_data["main_frame"]["stemheight"].set(self.config_object.get("default_stemheight")) # cm
        controller.shared_data["main_frame"]["barbottom"].set(round(controller.shared_data["main_frame"]["stemheight"].get()*self.config_object.get("initial_barbottomOverStemheight_coeff"),3)) # cm
        controller.shared_data["main_frame"]["barmiddle"].set(round(controller.shared_data["main_frame"]["barbottom"].get()+self.config_object.get("barradius"),3)) # cm
        controller.shared_data["main_frame"]["passfillednames_checkbox"].set(1)
        controller.shared_data["main_frame"]["timestring"].set(time.strftime("%H%M"))
        controller.shared_data["main_frame"]["currentdirection"].set("")
        controller.shared_data["main_frame"]["addressInput"].set("")
        
        if self.config_object.get("autopopulatestemcount") == True:
            controller.shared_data["main_frame"]["cell1"]["count"].set(self.config_object.get("defaultstemcount")),
            controller.shared_data["main_frame"]["cell2"]["count"].set(self.config_object.get("defaultstemcount")),
            controller.shared_data["main_frame"]["cell3"]["count"].set(self.config_object.get("defaultstemcount")),
            controller.shared_data["main_frame"]["cell4"]["count"].set(self.config_object.get("defaultstemcount")),
            controller.shared_data["main_frame"]["cell5"]["count"].set(self.config_object.get("defaultstemcount")),
            controller.shared_data["main_frame"]["cell6"]["count"].set(self.config_object.get("defaultstemcount")),
            controller.shared_data["main_frame"]["cell7"]["count"].set(self.config_object.get("defaultstemcount")),
            controller.shared_data["main_frame"]["cell8"]["count"].set(self.config_object.get("defaultstemcount")),
            controller.shared_data["main_frame"]["cell9"]["count"].set(self.config_object.get("defaultstemcount"))
        ''' end '''



# buttons that are the same for each page
#'''
class RepeatPageButtons:
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
