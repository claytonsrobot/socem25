# __main__.py
from socem25.shell.shell import SocemCLI
from socem25.core.directories import Directories
def cli_entry():
    #try:
    if True:
        # Launch the cmd2 terminal
        Directories.initialize_program_dir()
        app = SocemCLI()
        app.run()
    #except Exception as e:
    #    print(f"An error occurred: {e}")

if __name__ == "__main__":
    cli_entry()
