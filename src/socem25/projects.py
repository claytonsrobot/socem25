# src/socem25/projects.py

from pathlib import Path

class ProjectManager:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.projects = []

    def load_projects(self):
        self.projects = [p for p in self.base_dir.iterdir() if p.is_dir()]