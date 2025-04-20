# __main__.py
#from socem25.core import stemberry
import socem25.core.main_funcs
import tkinter as tk
from pprint import pprint as pprint
def cli_entry():
    try:
        # Launch main
        #src.main.run()
        socem25.core.main_funcs.run()
        #shell.shell.main()
    except Exception as e:
        print(f"An error occurred: {e}")

def cli_entry():
    parent = tk.Tk()  # Creating the main window
    controller = None  # Define your controller object or pass as needed
    app = SocemGuiMain(parent, controller)  # Pass both parent and controller
    app.run()  # Call the run method to start the application
    app.mainloop()  # Start the Tkinter main event loop

if __name__ == "__main__":
    app = cli_entry()
    print(f"app = {app}")
    #print(f"app.__doc__ = {app.__doc__}")
    pprint(app.__doc__)