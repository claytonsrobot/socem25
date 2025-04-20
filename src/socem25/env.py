# src/socem25/env.py

from pathlib import Path

class Env:
    def __init__(self, root_path: Path):
        self.root_path = root_path
        self.mode = "development"  # stub value