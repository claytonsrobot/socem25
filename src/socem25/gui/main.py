# src/socem25/gui/main.py

from socem25.startup import Startup

def run_gui():
    app = Startup()
    app.startup()

    print("🚀 GUI launched — would display Qt window here.")

    app.shutdown()

if __name__ == "__main__":
    run_gui()