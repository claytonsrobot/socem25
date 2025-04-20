# core.config_manager.py
import os
import toml
import shutil
from pprint import pprint
from datetime import date
import math
import socem25.core.helpers.toml_utils
from socem25.core.directories import Directories


class Config:
    def __init__(self, project=None, config_filepath=None):
        self.project = project or "default"
        self.config_filepath = config_filepath or Directories.get_config_entry()
        self.loaded_config = {}
        self.flexural_params = {}
        self.expressions = {}

        # Initialize Directories
        Directories.initialize_program_dir()
        Directories.initialize_startup_project()

        # Load and process the configuration
        self.load_config()
        self.evaluate_expressions()

    def load_config(self):
        """Loads the configuration file and processes it."""
        try:
            raw_loaded_config = toml.load(self.config_filepath)
            self.loaded_config = raw_loaded_config.get("config", {})
            self.flexural_params = raw_loaded_config.get("flexural_rigidity_parameters", {})
            self._original_loaded_config = self.loaded_config.copy()
        except FileNotFoundError:
            print(f"[Config] Configuration file not found: {self.config_filepath}")
            self.loaded_config = {}
        except toml.TomlDecodeError:
            print(f"[Config] Error decoding TOML file: {self.config_filepath}")
            self.loaded_config = {}

    @property
    def today(self):
        """Return the current date."""
        return date.today().strftime("%b-%d-%Y")

    @property
    def inchonvert(self):
        """Calculate the inch conversion."""
        return (math.pi * 0.764 * 31.4136) / 359

    def clean_imported_numerics(self, loaded_config):
        """Cleans numeric values from the configuration dictionary."""
        return {
            key: (int(value) if value.isdigit() else float(value) if self.is_float(value) else value)
            for key, value in loaded_config.items()
        }

    @staticmethod
    def is_float(value):
        """Check if the value can be converted to a float."""
        try:
            float(value)
            return True
        except ValueError:
            return False

    def save_config(self, confirm=False, backup=True):
        """Saves the configuration to the file."""
        if self.loaded_config == self._original_loaded_config:
            print("[Config] No changes detected. Skipping save.")
            return

        if confirm and input(f"Changes detected. Overwrite {self.config_filepath}? (y/n): ").lower() != 'y':
            print("[Config] Save cancelled by user.")
            return

        if backup:
            self.create_backup()

        try:
            with open(self.config_filepath, 'w') as f:
                toml.dump({
                    "config": self.loaded_config,
                    "flexural_rigidity_parameters": self.flexural_params
                }, f)
            print(f"[Config] Changes saved to {self.config_filepath}")
            self._original_loaded_config = self.loaded_config.copy()
        except Exception as e:
            print(f"[Config] Failed to save config: {e}")

    def create_backup(self):
        """Creates a backup of the config file."""
        backup_path = self.config_filepath + ".bak"
        try:
            shutil.copyfile(self.config_filepath, backup_path)
            print(f"[Config] Backup saved to {backup_path}")
        except Exception as e:
            print(f"[Config] Warning: Could not create backup: {e}")

    def load_and_process_default_config(self):
        """Loads the default configuration and processes it."""
        print("Loading and defining default config input...")
        raw_loaded_config = socem25.core.helpers.toml_utils.load_toml(self.config_filepath)["config"]
        self.loaded_config = self.clean_imported_numerics(raw_loaded_config)

        # Load grouping entry and process accordingly
        self.grouping_selection_path, self.grouping_algorithm = self.load_grouping_entry()
        
        if self.grouping_algorithm == "group-by-text":
            self.raw_loaded_grouping = socem25.core.helpers.toml_utils.load_toml(self.grouping_selection_path)
            self.loaded_grouping = self.raw_loaded_grouping["grouping"].copy()
            socem25.core.json_handler.export_to_json(self.loaded_grouping, Directories.get_group_by_text_intermediate_export_json_filepath())
        
        pprint(f"Loaded config: {self.loaded_config}")
        return self.loaded_config
