'''
controller.py
'''
import tkinter as tk
from socem25.gui.gui_main import SocemGuiMain
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Socem25")

        self.shared_data = {}
        self.shared_data["main_frame"]
        main_window = SocemGuiMain(None,self)

    def register_variable_dictionaries_and_keys(self):
        self.register_main_frame_vars()
        self.register_final_inputs_frame_vars()
        self.register_initial_inputs_frame_vars()
        self.register_record_force_frame_vars()
        
    def register_main_frame_vars(self):
        self.shared_data["main_frame"] = {}
        
    def register_final_inputs_frame_vars(self):
        self.shared_data["final_frame"] = {}

    def register_initial_inputs_frame_vars(self):
        self.shared_data["initial_frame"] = {}

    def register_record_force_frame_vars(self):
        self.shared_data["record_frame"] = {}

    
if __name__ == "__main__":
    app = App()
    app.mainloop()