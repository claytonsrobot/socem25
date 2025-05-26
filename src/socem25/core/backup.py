import datetime
import time

import socem25.core.environment
from socem25.core.environment import Env
#from gui_main import SocemGuiMain
from socem25.core.pass_in import PassIn


class Backup(PassIn):
    def createBackupFile(self, controller):
        ''' Create a temp text file, with a list of all variables and variable names, that would be awesome '''
        '''update_filename_preTest()
        update_filename_postTest()
        sniff_filename_force()
        update_filename_postTest()
        saveState_update_filenames()'''
        now = datetime.datetime.now()
        unix_now = time.mktime(now.timetuple())
        unix_now_int = int(unix_now) # still gets seconds # the purpose of this is to append to filenames
        str(unix_now_int)
        filename_savestate = "backup_stemberry_"+str(unix_now_int)+".txt"
        filename_savestate_full = self.gui_main_object.address+"/"+filename_savestate
        print("State saved at "+str(datetime.datetime.fromtimestamp(unix_now_int))+": "+filename_savestate)
        # list all GUI vars, add them to a txt file
        self.gui_main_object.masslist=[controller.shared_data["main_frame"]["cell1"]["mass"].get(),controller.shared_data["main_frame"]["cell2"]["mass"].get(),controller.shared_data["main_frame"]["cell3"]["mass"].get(),controller.shared_data["main_frame"]["cell4"]["mass"].get(),controller.shared_data["main_frame"]["cell5"]["mass"].get(),controller.shared_data["main_frame"]["cell6"]["mass"].get(),controller.shared_data["main_frame"]["cell7"]["mass"].get(),controller.shared_data["main_frame"]["cell8"]["mass"].get(),controller.shared_data["main_frame"]["cell9"]["mass"].get()] 
        self.gui_main_object.stemcounts=[controller.shared_data["main_frame"]["cell1"]["count"].get(),controller.shared_data["main_frame"]["cell2"]["count"].get(),controller.shared_data["main_frame"]["cell3"]["count"].get(),controller.shared_data["main_frame"]["cell4"]["count"].get(),controller.shared_data["main_frame"]["cell5"]["count"].get(),controller.shared_data["main_frame"]["cell6"]["count"].get(),controller.shared_data["main_frame"]["cell7"]["count"].get(),controller.shared_data["main_frame"]["cell8"]["count"].get(),controller.shared_data["main_frame"]["cell9"]["count"].get()] 
        self.gui_main_object.diameters_cell1 = [controller.shared_data["main_frame"]["cell1"]["diameter1"].get(),controller.shared_data["main_frame"]["cell1"]["diameter2"].get(),controller.shared_data["main_frame"]["cell1"]["diameter3"].get(),controller.shared_data["main_frame"]["cell1"]["diameter4"].get()]
        self.gui_main_object.diameters_cell2 = [controller.shared_data["main_frame"]["cell2"]["diameter1"].get(),controller.shared_data["main_frame"]["cell2"]["diameter2"].get(),controller.shared_data["main_frame"]["cell2"]["diameter3"].get(),controller.shared_data["main_frame"]["cell2"]["diameter4"].get()]
        self.gui_main_object.diameters_cell3 = [controller.shared_data["main_frame"]["cell3"]["diameter1"].get(),controller.shared_data["main_frame"]["cell3"]["diameter2"].get(),controller.shared_data["main_frame"]["cell3"]["diameter3"].get(),controller.shared_data["main_frame"]["cell3"]["diameter4"].get()]
        self.gui_main_object.diameters_cell4 = [controller.shared_data["main_frame"]["cell4"]["diameter1"].get(),controller.shared_data["main_frame"]["cell4"]["diameter2"].get(),controller.shared_data["main_frame"]["cell4"]["diameter3"].get(),controller.shared_data["main_frame"]["cell4"]["diameter4"].get()]
        self.gui_main_object.diameters_cell5 = [controller.shared_data["main_frame"]["cell5"]["diameter1"].get(),controller.shared_data["main_frame"]["cell5"]["diameter2"].get(),controller.shared_data["main_frame"]["cell5"]["diameter3"].get(),controller.shared_data["main_frame"]["cell5"]["diameter4"].get()]
        self.gui_main_object.diameters_cell6 = [controller.shared_data["main_frame"]["cell6"]["diameter1"].get(),controller.shared_data["main_frame"]["cell6"]["diameter2"].get(),controller.shared_data["main_frame"]["cell6"]["diameter3"].get(),controller.shared_data["main_frame"]["cell6"]["diameter4"].get()]
        self.gui_main_object.diameters_cell7 = [controller.shared_data["main_frame"]["cell7"]["diameter1"].get(),controller.shared_data["main_frame"]["cell7"]["diameter2"].get(),controller.shared_data["main_frame"]["cell7"]["diameter3"].get(),controller.shared_data["main_frame"]["cell7"]["diameter4"].get()]
        self.gui_main_object.diameters_cell8 = [controller.shared_data["main_frame"]["cell8"]["diameter1"].get(),controller.shared_data["main_frame"]["cell8"]["diameter2"].get(),controller.shared_data["main_frame"]["cell8"]["diameter3"].get(),controller.shared_data["main_frame"]["cell8"]["diameter4"].get()]
        self.gui_main_object.diameters_cell9 = [controller.shared_data["main_frame"]["cell9"]["diameter1"].get(),controller.shared_data["main_frame"]["cell9"]["diameter2"].get(),controller.shared_data["main_frame"]["cell9"]["diameter3"].get(),controller.shared_data["main_frame"]["cell9"]["diameter4"].get()]

        lines = [
            'Units: diameter (mm), height (cm), range (cm), length (cm), mass (g), time (sec), force (N) \n',
            'script = '+script,
            'directory = '+directory+'/',
            'operatingsystem = '+Env.get_operatingsystem(),
            'os.getlogin() = '+os.getlogin(),
            'operator = '+operator,
            'location = '+location,
            'coordinates = '+coordinates,
            'self.gui_main_object.ignoreserial = '+str(self.gui_main_object.ignoreserial),
            'default_stemheight = '+str(default_stemheight),
            'calibrationFactor = '+str(calibrationFactor),
            'encoderWorked_override = '+str(encoderWorked_override),
            'assessAllTests = '+str(assessAllTests),
            'barlength = '+str(barlength),
            'datestring = '+Env.datestring,
            'unix_now_int = '+str(unix_now_int),
            'backup filename unix_now_int decoded: '+ str(datetime.datetime.fromtimestamp(unix_now_int))+'\n',
            'self.gui_main_object.timestring.get() = '+self.gui_main_object.timestring.get(),
            'self.gui_main_object.errors = '+makeDataString(self.gui_main_object.errors),
            'self.gui_main_object.errorCodes = '+makeDataString(self.gui_main_object.errorCodes),
            'self.gui_main_object.varietyname.get() = '+self.gui_main_object.varietyname.get(),
            'self.gui_main_object.plotname.get() = '+self.gui_main_object.plotname.get(),
            'self.gui_main_object.currentdirection.get() = '+self.gui_main_object.currentdirection.get(),
            'self.gui_main_object.filename_force.get() = '+self.gui_main_object.filename_force.get(),
            'self.gui_main_object.filename_preTest.get() = '+self.gui_main_object.filename_preTest.get(),
            'self.gui_main_object.filename_postTest.get() = '+self.gui_main_object.filename_postTest.get(),
            'self.gui_main_object.stemheight.get() = '+str(self.gui_main_object.stemheight.get()),
            'self.gui_main_object.barmiddle.get() = '+str(self.gui_main_object.barmiddle.get()),
            'self.gui_main_object.barbottom.get() = '+str(self.gui_main_object.barbottom.get()),
            'self.gui_main_object.passfillednames_checkbox.get() = '+str(self.gui_main_object.passfillednames_checkbox.get()),
            'self.gui_main_object.startRange1.get() = '+str(self.gui_main_object.startRange1.get()),
            'self.gui_main_object.startRange2.get() = '+str(self.gui_main_object.startRange2.get()),
            'self.gui_main_object.startRange3.get() = '+str(self.gui_main_object.startRange3.get()),
            'self.gui_main_object.travelvelocity = '+str(self.gui_main_object.travelvelocity),
            'self.gui_main_object.samplingrate = '+str(self.gui_main_object.samplingrate),
            'self.gui_main_object.masslist = '+makeDataString(self.gui_main_object.masslist),
            'self.gui_main_object.stemcounts = '+makeDataString(self.gui_main_object.stemcounts),
            'self.gui_main_object.diameters_cell1 = '+makeDataString(self.gui_main_object.diameters_cell1),
            'self.gui_main_object.diameters_cell2 = '+makeDataString(self.gui_main_object.diameters_cell2),
            'self.gui_main_object.diameters_cell3 = '+makeDataString(self.gui_main_object.diameters_cell3),
            'self.gui_main_object.diameters_cell4 = '+makeDataString(self.gui_main_object.diameters_cell4),
            'self.gui_main_object.diameters_cell5 = '+makeDataString(self.gui_main_object.diameters_cell5),
            'self.gui_main_object.diameters_cell6 = '+makeDataString(self.gui_main_object.diameters_cell6),
            'self.gui_main_object.diameters_cell7 = '+makeDataString(self.gui_main_object.diameters_cell7),
            'self.gui_main_object.diameters_cell8 = '+makeDataString(self.gui_main_object.diameters_cell8),
            'self.gui_main_object.diameters_cell9 = '+makeDataString(self.gui_main_object.diameters_cell9),
            'self.gui_main_object.EI_fullcontact = '+makeDataString(self.gui_main_object.EI_fullcontact),
            'self.gui_main_object.EI_intermediatecontact = '+makeDataString(self.gui_main_object.EI_intermediatecontact),
            'self.gui_main_object.EI_nocontact = '+makeDataString(self.gui_main_object.EI_nocontact),
            'self.gui_main_object.AvgEI_intermediatecontact = '+makeDataString(self.gui_main_object.AvgEI_intermediatecontact),
            str(datetime.datetime.now())+'\n']
        
        evenmorelines = [
            'self.gui_main_object.filename_all.get() = '+self.gui_main_object.filename_all.get(), # no longer exists, compilation XLSX
            'self.gui_main_object.distanceTraveled = '+makeDataString(self.gui_main_object.distanceTraveled),
            'self.gui_main_object.forcePushed = '+makeDataString(self.gui_main_object.forcePushed),
            'self.gui_main_object.timeElapsed = '+makeDataString(self.gui_main_object.timeElapsed)+'\n',
            'Collected data, nine cell scheme:',
            'self.gui_main_object.forcePushed_side1 = '+makeDataString(self.gui_main_object.forcePushed_side1),
            'self.gui_main_object.distanceTraveled_side1 = '+makeDataString(self.gui_main_object.distanceTraveled_side1),
            'self.gui_main_object.timeElapsed_side1 = '+makeDataString(self.gui_main_object.timeElapsed_side1),
            'self.gui_main_object.forcePushed_side2 = '+makeDataString(self.gui_main_object.forcePushed_side2),
            'self.gui_main_object.distanceTraveled_side2 = '+makeDataString(self.gui_main_object.distanceTraveled_side2),
            'self.gui_main_object.timeElapsed_side2 = '+makeDataString(self.gui_main_object.timeElapsed_side2),
            'self.gui_main_object.forcePushed_side3 = '+makeDataString(self.gui_main_object.forcePushed_side3),
            'self.gui_main_object.distanceTraveled_side3 = '+makeDataString(self.gui_main_object.distanceTraveled_side3),
            'self.gui_main_object.timeElapsed_side3 = '+makeDataString(self.gui_main_object.timeElapsed_side3),
            'self.gui_main_object.forcePushed_forward = '+makeDataString(self.gui_main_object.forcePushed_forward),
            'self.gui_main_object.distanceTraveled_forward = '+makeDataString(self.gui_main_object.distanceTraveled_forward),
            'self.gui_main_object.timeElapsed_forward = '+makeDataString(self.gui_main_object.timeElapsed_forward),
            str(datetime.datetime.now())]
            
        try:
            morelines = [
                '\n',
                'RecordForce.ser = '+str(RecordForce.ser),
                str(datetime.datetime.now())]
        except:
            morelines = [
                '\n',
                'RecordForce.ser = '+'error',
                str(datetime.datetime.now())]
        
        with open(filename_savestate_full, 'w') as f:
            f.write('\n'.join(lines))
            f.write('\n'.join(morelines))
            try:
                f.write('\n'.join(evenmorelines))
            except:
                pass

    def makeDataString(dataVector):
        #timeElapsed_string = ' '.join(str(e) for e in self.gui_main_object.timeElapsed)
        dataString = ', '.join(str(e) for e in dataVector)
        dataString = '[' + dataString + ']'
        
        return dataString

    def restoreState():
        print("Please develop. Not yet functional for setting tkinter variables.")
        # choose txt file (example: backup_stemberry_1660192559.txt
        # trigger GUI directory and file selection would be sick.
        # only restore postTest fields? start there.
        # change each instance of '.get() = x' to '.set(x)'
        '''
        filename_savestate = "backup_stemberry_"+str(unix_now_int)+".txt"
        filename_savestate_full = self.gui_main_object.address+"/"+filename_savestate
        '''
        filename_restorestate = (str(input('Restore backup filename: ')))

        #with open('readme.txt') as f:
        with open(self.gui_main_object.address+"/"+filename_restorestate) as f:
            lines = f.readlines()
            
    def importFileData():
        print("Please develop.")
        # imort data from csv files