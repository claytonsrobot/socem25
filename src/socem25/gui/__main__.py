# __main__.py
import tkinter as tk
from socem25.gui.gui_main import SocemGuiMain
from socem25.core.directories import Directories
from socem25.core.configuration import Config
def cli_entry():
    parent = tk.Tk()
    controller = None
    Directories.initialize_program_dir()
    Directories.initialize_startup_project()

    config_path = Directories.get_config_entry()
    config_object = Config(filepath=config_path)  # Instantiate the Config class

    app = SocemGuiMain(parent,controller)
    app.pass_in_config_object(config_object)
    app.run()
    app.mainloop()

if __name__ == "__main__":
    cli_entry()
