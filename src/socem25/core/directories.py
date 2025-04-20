"""
Title: directories.py
Author: Clayton Bennett
Created: 29 January 2025

Purpose: 
Keep directory assignment organized, particularly for using project folders.
Migrate away from directory amangement in environmental.py

Example:
from socem25.core.directories import Directories

"""
import os
import inspect
from socem25.core.helpers import toml_utils
import socem25.core.environment

class Directories:
    "from socem25.core.directories import Directories"

    program = None
    project = None
    root = None
    config_entry_filepath = "./projects/default-project.toml"

    # ----- Setters -----
    @classmethod
    def set_program_dir(cls, path):
        cls.program = os.path.normpath(path)

    @classmethod
    def set_project_dir(cls, path):
        if os.path.isdir(path):
            cls.project = os.path.normpath(path)
        else:
            # assume it's a project name, not a full path
            relative_path = os.path.join(cls.program, "projects", path)
            if os.path.isdir(relative_path):
                cls.project = os.path.normpath(relative_path)
        print(f"[Directories] Project directory set: {cls.project}")

    # ----- Getters -----
    @classmethod
    def get_program_dir(cls):
        return cls.program

    @classmethod
    def get_project_dir(cls):
        return cls.project

    @classmethod
    def get_config_dir(cls):
        return os.path.join(cls.project, "configs")

    @classmethod
    def get_export_dir(cls):
        return os.path.join(cls.project, "exports")

    @classmethod
    def get_import_dir(cls):
        return os.path.join(cls.project, "imports")

    @classmethod
    def get_groupings_dir(cls):
        return os.path.join(cls.get_config_dir(), "groupings")

    @classmethod
    def get_intermediate_group_structure_export_dir(cls):
        return os.path.join(cls.get_groupings_dir(), "intermediate_group_structure_export")

    @classmethod
    def get_group_by_directory_intermediate_export_json_filepath(cls):
        return os.path.join(cls.get_intermediate_group_structure_export_dir(), "group_by_directory_intermediate_export.json")

    @classmethod
    def get_group_by_spreadsheet_intermediate_export_json_filepath(cls):
        return os.path.join(cls.get_intermediate_group_structure_export_dir(), "group_by_spreadsheet_intermediate_export.json")

    @classmethod
    def get_group_by_text_intermediate_export_json_filepath(cls):
        return os.path.join(cls.get_intermediate_group_structure_export_dir(), "group_by_text_intermediate_export.json")

    # ----- Initialization -----
    @classmethod
    def initialize_program_dir(cls):
        cls.set_program_dir(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
        print(f"[Directories] Program directory initialized: {cls.get_program_dir()}")

    @classmethod
    def initialize_startup_project(cls):
        loaded_entry = toml_utils.load_toml(cls.config_entry_filepath)
        project_folder = loaded_entry["project_directory"]
        cls.set_project_dir(os.path.join(cls.get_program_dir(), "projects", project_folder))

    # ----- Config File Entry -----
    @classmethod
    def get_config_entry(cls):
        loaded_entry = toml_utils.load_toml(cls.config_entry_filepath)
        config_filename = loaded_entry["entry"]["config_input_filename"]
        config_path = os.path.normpath(os.path.join(cls.get_config_dir(), config_filename))
        cls.check_file(config_path)
        return config_path

    # ----- Utility -----
    @staticmethod
    def check_file(filepath):
        if not os.path.isfile(filepath):
            print(f"[Directories] File does not exist: {filepath}")
            raise SystemExit
        return True
def bless_this_mess():
    if socem25.core.environment.get_operatingsystem() == 'Windows':
        if os.getlogin() == 'clayt':
            address = r'C:\Users\clayton\OneDrive - University of Idaho\AqMEQ\SOCEM\Data - Instron and SOCEM - 2020, 2021\SOCEM_DATA_2021'
            dev_guess = 'COM3' # manual override, windows 10 OS
        else:
            #dev_manualOverride = False
            address = directory + '/SOCEM_data'
            if not os.path.exists(address):
                os.makedirs(address) 
    elif socem25.core.environment.get_operatingsystem() == 'Linux':
        dev_guess = '/dev/ttyACM0' # manual override raspian OS
        address = '/home/pi/Desktop/SOCEM_data_2022'
    else:
        address = directory + '/SOCEM_data'
        dev_guess = dev_manual
        dev_manualOverride = False
        if not os.path.exists(address):
            os.makedirs(address)