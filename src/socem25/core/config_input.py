'''
Title:config_input
Author: Clayton Bennett
Created: 01 June 2024

'''
#import numpy as np
import os
from pprint import pprint

#import inspect
#import json
#import environmental
#import platform # assumes local is windows and server is linux for vercel
from socem25.core.directories import Directories
import socem25.core.helpers.toml_utils


class ConfigInput:
    """
    This class handles the loading of configuration files, applying grouping logic, and
    managing TOML file inputs. It integrates with the Directories module for
    file management and provides methods to clean numeric values in config data.
    """

    config_entry_filename = r"config_entry.toml"
    grouping_entry_filename = r"grouping_entry.toml"
    
    def __init__(self):
        self.script_dir = Directories.get_program_dir()
        self.config_directory = Directories.get_config_dir()
        self.config_entry_filepath = os.path.join(self.config_directory, self.config_entry_filename)
        self.grouping_entry_filepath = os.path.join(self.config_directory, self.grouping_entry_filename)
        
        # Validate configuration files
        Directories.check_file(self.config_entry_filepath)
        Directories.check_file(self.grouping_entry_filepath)

        # Initialize variables
        self.loaded_config = None
        self.grouping_algorithm = None
        self.grouping_selection_path = None
        self.loaded_grouping = None

    def load_config_entry(self):
        """
        Loads the configuration file as defined in the config_entry.toml and returns
        the path to the actual configuration file.

        Returns:
            str: The path to the configuration file.
        """
        loaded_config_entry_toml = socem25.core.helpers.toml_utils.load_toml(self.config_entry_filepath)
        config_input_filename = loaded_config_entry_toml["entry"]["config_input_filename"]
        config_input_path = os.path.join(Directories.get_config_dir(), config_input_filename)
        Directories.check_file(config_input_path)
        return config_input_path
    
    def load_grouping_entry(self):
        """
        Loads the grouping entry file and returns the path to the grouping selection
        file along with the selected grouping algorithm.

        Returns:
            tuple: (grouping_selection_path (str), grouping_algorithm (str))
        """
        loaded_grouping_entry_toml = socem25.core.helpers.toml_utils.load_toml(self.grouping_entry_filepath)
        grouping_selection_filename = loaded_grouping_entry_toml["grouping"]["grouping_selection_filename"]
        grouping_algorithm = loaded_grouping_entry_toml["grouping"]["algorithm"]
        grouping_selection_path = None if grouping_selection_filename is None else os.path.join(Directories.get_groupings_dir(), grouping_selection_filename)
        
        if grouping_selection_path:
            Directories.check_file(grouping_selection_path)
        
        return grouping_selection_path, grouping_algorithm

    def clean_imported_numerics(self, loaded_config):
        """
        Converts any numeric strings in the config dictionary to integers or floats.
        
        Args:
            loaded_config (dict): The configuration dictionary.
        
        Returns:
            dict: The cleaned configuration dictionary with numeric values converted.
        """
        for key, value in loaded_config.items():
            if isinstance(value, str) and value.isnumeric():
                try:
                    loaded_config[key] = int(value)
                except ValueError:
                    loaded_config[key] = float(value)
        return loaded_config

    def define_and_load_default_config_input(self):
        """
        Loads the default configuration and grouping entry, processes the configuration data,
        and prepares it for use in the application.

        Returns:
            tuple: (loaded_config (dict), loaded_grouping (dict))
        """
        print("Loading and defining default config input...")
        config_input_path = self.load_config_entry()
        self.grouping_selection_path, self.grouping_algorithm = self.load_grouping_entry()
        
        # Load the main configuration and clean numeric values
        raw_loaded_config = socem25.core.toml_utils.load_toml(config_input_path)["config"]
        self.loaded_config = self.clean_imported_numerics(raw_loaded_config)
        
        # Handle grouping based on algorithm selected
        if self.grouping_algorithm == "group-by-text":
            self.raw_loaded_grouping = socem25.core.helpers.toml_utils.load_toml(self.grouping_selection_path)
            self.loaded_grouping = self.raw_loaded_grouping["grouping"].copy()
            socem25.core.json_handler.export_to_json(self.loaded_grouping, Directories.get_group_by_text_intermediate_export_json_filepath())
        
        elif self.grouping_algorithm == "group-by-spreadsheet":
            self.loaded_grouping = self.load_csv(self.grouping_selection_path)
            socem25.core.json_handler.export_to_json(self.loaded_grouping, Directories.get_group_by_spreadsheet_intermediate_export_json_filepath())
        
        elif self.grouping_algorithm == "group-by-directory":
            print("Grouping by directory...")
            self.loaded_grouping = socem25.core.grouping_by_directory.call(directory_path=Directories.get_import_dir())

        # Set some default values in the config
        self.loaded_config["filter_files_include_and"] = ""
        self.loaded_config["filter_files_include_or"] = ""
        self.loaded_config["filter_files_exclude"] = ""
        self.loaded_config["export_directory"] = ""

        pprint(f"Loaded config: {self.loaded_config}")
        return self.loaded_config, self.loaded_grouping


if __name__ == "__main__":
    config_directory = Directories.get_config_dir()
    filename = r"gui_defaults_01June24.json"
    filepath = os.path.join(config_directory, filename)
    filepath = os.path.normpath(filepath)

    config_input_object = ConfigInput()
    loaded_config = socem25.core.helpers.toml_utils.load_toml(filepath)
    
    print('\nLoaded config keys:')
    print(loaded_config.keys())
    print('\n')

    # Example usage of ConfigInput methods
    config_input_object.define_and_load_default_config_input()
