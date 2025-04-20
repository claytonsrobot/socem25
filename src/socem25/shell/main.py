from socem25.startup import Startup

def cli():
    app = Startup()
    app.startup()

    # fake CLI loop
    print("Welcome to the CLI. Loaded projects:", app.services.project_manager.projects)

    app.shutdown()

if __name__ == "__main__":
    cli()