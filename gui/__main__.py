# __main__.py
from gui.gui_main import SocemGuiMain
from src.directories import Directories
def cli_entry():
    #try:
    if True:
        # Launch the cmd2 terminal
        Directories.initilize_program_dir()
        app = SocemGuiMain()
        app.run()
    #except Exception as e:
    #    print(f"An error occurred: {e}")

if __name__ == "__main__":
    cli_entry()
