import argparse
import sys

def run_shell():
    from socem25.shell import main
    main.cli()

def run_gui():
    from socem25.gui import main
    main.run_gui()

def run_api():
    import uvicorn
    uvicorn.run("socem25.api.main:app", host="127.0.0.1", port=8000, reload=True)

def interactive_menu():
    print("\nWelcome to SOCEM 2.0 🎛️")
    print("Please select an interface:")
    print("1. Shell TUI")
    print("2. GUI")
    print("3. API Server")
    print("0. Exit")

    choice = input("Enter choice [0-3]: ").strip()

    if choice == "1":
        run_shell()
    elif choice == "2":
        run_gui()
    elif choice == "3":
        run_api()
    elif choice == "0":
        print("Goodbye!")
        sys.exit(0)
    else:
        print("Invalid choice.")
        interactive_menu()

def main():
    parser = argparse.ArgumentParser(description="SOCEM App Dispatcher")
    parser.add_argument("--mode", choices=["shell", "gui", "api"], help="Choose interface")

    args = parser.parse_args()

    if args.mode == "shell":
        run_shell()
    elif args.mode == "gui":
        run_gui()
    elif args.mode == "api":
        run_api()
    else:
        interactive_menu()

if __name__ == "__main__":
    main()
