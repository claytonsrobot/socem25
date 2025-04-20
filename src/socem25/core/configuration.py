"""
Title: configuration.py
Author: Clayton Bennett
Created 18 April 2025
"""

import platform
import toml
from pprint import pprint
from datetime import date
import math

import socem25.core.helpers.toml_utils
from socem25.core.directories import Directories

class Config:
    #defaultstemcount = 25
    #autopopulatestemcount = False
    def __init__(self, filepath=None):
        self.filepath = filepath or Directories.get_config_entry()
        self.loaded_config = {}
        self.load_config()

    def __init__(self, project="default"):
        self.project = project
        self.loaded_config = {}
        self.flexural_params = {}
        self.expressions = {}

        self.config_path = self._resolve_config_path()
        self.load_config()
        self.evaluate_expressions()

    def load_config(self):
        try:
            raw_loaded_config = toml.load(self.filepath)
            self.loaded_config = raw_loaded_config.get("config", {})
            self.flexural_params = raw_loaded_config.get("flexural_rigidity_parameters", {})
        except Exception as e:
            print(f"Failed to load config: {e}")
            self.loaded_config = {}

    def get(self, key, default=None):
        return self.loaded_config.get(key, default)

    def __getitem__(self, key):
        return self.get(key)

    def __str__(self):
        return f"Config({self.loaded_config})"
    
    def load_config_from_default(self):
        pass
    def load_config_from_project(self):
        pass

def define_and_load_default_config_input(self):
    "config_input.define_and_load_default_config_input()"
    # Load the config file
    raw_loaded_config = toml.load(Directories.get_config_entry())
    # Dynamically map the parsed config values to loaded_config
    self.loaded_config = {key: self.clean_imported_numerics(value) 
                          for key, value in raw_loaded_config.get("config", {}).items()}
    # Print and return the results
    #pprint(f"loaded_config = {self.loaded_config}")
    return self.loaded_config

def expressions(self):
    """math and dynamic expresions"""
    #print("os.getlogin() =",os.getlogin())
    #print("operator =",operator)
    #print("location =",location)
    self.today = date.today()
    self.datestring = self.today.strftime("%b-%d-%Y")
    self.inchonvert = (((math.pi*(0.764))*31.4136)/359) # converts displacement to inches, wheel diameter = 31.4136
    

if __name__ == "__main__":
    import os
    os.chdir("../..")
    config = Config()
    Directories.initialize_program_dir()
    Directories.initialize_startup_project()

    config_path = Directories.get_config_entry()
    cfg = Config(filepath=config_path)
    pprint(config.loaded_config)
    print("Today is:", config.get_expression("today"))
    print("Converted displacement to inches:", config.get_expression("inchonvert"))