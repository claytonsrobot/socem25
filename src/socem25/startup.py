# src/socem25/startup.py

from socem25.services import Services

class Startup:
    def __init__(self, config_path=None):
        self.services = Services(config_path=config_path)

    def startup(self):
        self.services.init_logger()
        self.services.init_environment()
        self.services.init_project_manager()
        self.services.logger.info("System startup complete.")

    def shutdown(self):
        self.services.logger.info("System shutting down.")