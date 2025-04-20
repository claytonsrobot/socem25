# __main__.py
import tkinter as tk
from socem25.gui.gui_main import SocemGuiMain
from socem25.core.directories import Directories
def cli_entry():
    parent = tk.Tk()
    controller = None
    Directories.initilize_program_dir()
    app = SocemGuiMain(parent,controller)
    app.run()
    app.mainloop()

if __name__ == "__main__":
    cli_entry()
