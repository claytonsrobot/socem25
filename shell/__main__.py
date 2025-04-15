# __main__.py
from shell.shell import SocemCLI

def cli_entry():
    try:
        # Launch the cmd2 terminal
        app = SocemCLI()
        app.run()
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    cli_entry()
