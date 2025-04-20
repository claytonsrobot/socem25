# __main__.py
#from socem25.core import stemberry
import socem25.core.main_funcs
from pprint import pprint as pprint
def cli_entry():
    try:
        # Launch main
        #src.main.run()
        socem25.core.main_funcs.run()
        #shell.shell.main()
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    app = cli_entry()
    print(f"app = {app}")
    #print(f"app.__doc__ = {app.__doc__}")
    pprint(app.__doc__)