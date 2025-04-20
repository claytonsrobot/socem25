import serial
#from serial import Serial
# from serial import *
import serial.tools.list_ports # need this
from socem25.core.pass_in import PassIn

class SerialConnection(PassIn):
    # Determine Arduino serial port address
    def serial_connect(self):
        #try:
        ports = serial.tools.list_ports.comports()
        try:
            dev = ports[0].device
        except:
            #dev = '/dev/ttyACM0' # only works on pi
            dev = self.config_object.get("dev_guess") # based on operating system
        if self.config_object.get("dev_manualOverride") == True:
            dev = self.config_object.get("dev_manual") # manual override
        try:
            ser = serial.Serial(dev, 115200, timeout=4,writeTimeout = 2,) # 1 second timeout
            #print(type(ser))
            print("dev = "+dev)
            ser.reset_input_buffer()  
            #ser.isOpen()
            #gui_main_object.ignoreserial = False
            return ser # this is the only spot it should be called ser, not RecordForce.ser
        
        except:
            self.gui_main_object.ignoreserial = True
            error = 'serial connection never established'
            eCode = 'e1' # eCode = e1
            self.gui_main_object.errors.append(error) # append error label
            self.gui_main_object.errorCodes.append(eCode) # append error code
            #popup('serial connection')
            print("eCode = "+eCode)

    # if serial disconnect (unplugged) reconnect - NOTE: doesn't properly work currently. 
    def serial_reconnect(self):
        print("serial_reconnect()")
        try:
        #if gui_main_object.ignoreserial == False:
            self.gui_main_object.ignoreserial = False
            try:
                self.gui_record_force_object.ser.close()
                self.gui_main_object.ignoreserial = False
            except:
                self.gui_main_object.ignoreserial = True
            self.gui_record_force_object.ser = self.serial_connect()
            
        except:
        #else:
            self.gui_main_object.ignoreserial = True
            print("\nYou hit the 'serial_reconnect' dropdown menu item while gui_main_object.ignoreserial == True.\nSerial cannot be reconnected because\neither an arduino is not connected to your computer\nor the arduino is not sought by StemBerry.")
            self.gui_record_force_object.message_connectArduino()