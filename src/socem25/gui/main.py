# src/socem25/gui/main.py

from socem25.startup import Startup

def run_gui():
    app = Startup() # there could be inherent limitations here - or - this could be an opportunity for a modular software bridge.
    app.startup()

    print("🚀 GUI launched — would display Qt window here.")
    app.run()

    app.shutdown()

def main():
    run_gui()
if __name__ == "__main__":
    main()