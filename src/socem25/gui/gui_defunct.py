import tkinter as tk
from socem25.gui.gui_main import RepeatPageButtons
from socem25.core.pass_in import PassIn
import socem25.core.main_funcs

class StemCountClassic(PassIn, tk.Frame):
    def __init__(self, parent, controller):
        # Call PassIn's constructor with parent
        PassIn.__init__(self, parent)
        # Initialize tk.Frame
        tk.Frame.__init__(self, parent)
        
        header_label = tk.Label(self, text = "STEM COUNT INITIAL INPUT", font = ("arial", 17, "bold"), fg = "gray3", bg="ghost white")
        construction_label = tk.Label(self, text = "Under Construction.\nWill allow user to input sample density data before pushing SOCEM,\nrather than use the nine-cell post test count input fields.", font = ("arial", 17, "bold"), fg = "red4", bg="ghost white")
        header_label.place(x=235,y=0)
        construction_label.place(x=10,y=100)
        
        pageButtons = RepeatPageButtons.showButtons(self, parent, controller)
'''
class Heights(tk.Frame):
    destroyed. see StemBerry_v13.
'''