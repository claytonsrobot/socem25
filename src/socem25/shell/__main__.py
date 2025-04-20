# __main__.py
from shell.shell import SocemCLI
from src.directories import Directories
def cli_entry():
    #try:
    if True:
        # Launch the cmd2 terminal
        Directories.initilize_program_dir()
        app = SocemCLI()
        app.run()
    #except Exception as e:
    #    print(f"An error occurred: {e}")

if __name__ == "__main__":
    cli_entry()
