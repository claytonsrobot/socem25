# src/socem25/services.py

from pathlib import Path
from socem25.env import Env
from socem25.projects import ProjectManager
from socem25.logging_utils import setup_logger

class Services:
    def __init__(self, config_path: Path = None):
        self.config_path = config_path or Path.cwd() / "config.yaml"
        self.env = None
        self.project_manager = None
        self.logger = None

    def init_logger(self):
        self.logger = setup_logger()

    def init_environment(self):
        self.env = Env(root_path=Path.cwd())

    def init_project_manager(self):
        self.project_manager = ProjectManager(Path.cwd() / "projects")