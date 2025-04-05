# __main__.py
from shell import main

def cli_entry():
    try:
        # Launch main
        main()
        #shell.shell.main()
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    cli_entry()
