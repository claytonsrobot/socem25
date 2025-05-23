import os
from socem25.startup import Startup

def cli():
    app = Startup()
    app.startup()

    # fake CLI loop
    print("Welcome to the CLI. Loaded projects:", [os.path.basename(p) for p in app.services.project_manager.projects])

    app.shutdown()

def main():
    cli()

if __name__ == "__main__":
    main()