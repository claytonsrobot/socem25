"""
Title: directories.py
Author: Clayton Bennett
Created: 29 January 2025

Purpose: 
Keep directory assignment organized, particularly for using project folders.
Migrate away from directory amangement in environmental.py

Example:
from src.directories import Directories

"""
import os
import inspect
from src.helpers import toml_utils
from src import environmental

class Directories:
    core = None
    project = None
    configs = None
    exports = None
    imports = None
    groupings = None

    """ setters """
    @classmethod
    def set_core_dir(cls,path):
        cls.core = path
    @classmethod
    def set_project_dir(cls,path):
        # if a legitimate full path is not provided, assume that the project directory is within the core\projects\ directory
        if os.path.isdir(path):
            cls.project = path
        else:
            relative_path =  cls.get_core_dir()+"\\projects\\"+path
            if os.path.isdir(relative_path):
                cls.project = relative_path
        print(f"Project directory set: {cls.project}")

    """ getters """
    @classmethod
    def get_core_dir(cls):
        #return cls.core
        return cls.core
    @classmethod
    def get_program_dir(cls):
        return cls.get_core_dir()
    @classmethod
    def get_project_dir(cls):
        return cls.project
    @classmethod
    def get_config_dir(cls):
        return cls.get_project_dir()+"\\configs\\"
    @classmethod
    def get_export_dir(cls):
        return cls.get_project_dir()+"\\exports\\"
    @classmethod
    def get_import_dir(cls):
        if environmental.vercel==False:
            return cls.get_project_dir()+"\\imports\\"
        elif environmental.vercel==True: # web app, blob
            print("\nYou have not yet built a web app, last I checked.\nAnd yet, environmental.vercel==True")
            pass
        return cls.get_project_dir()+"\\imports\\"
    @classmethod
    def get_groupings_dir(cls):
        return cls.get_config_dir()+"\\groupings\\"
    @classmethod
    def get_intermediate_group_structure_export_dir(cls):
        return cls.get_groupings_dir()+"\\intermediate_group_structure_export\\"
    @classmethod
    def get_group_by_directory_intermediate_export_json_filepath(cls):
        return cls.get_intermediate_group_structure_export_dir()+"group_by_directory_intermediate_export.json"
    @classmethod
    def get_group_by_spreadsheet_intermediate_export_json_filepath(cls):
        return cls.get_intermediate_group_structure_export_dir()+"group_by_spreadsheet_intermediate_export.json"
    @classmethod
    def get_group_by_text_intermediate_export_json_filepath(cls):
        return cls.get_intermediate_group_structure_export_dir()+"group_by_text_intermediate_export.json"
    
    # migrated
    @classmethod
    def initilize_program_dir(cls): # called in CLI. Should also be called at other entry points.
        cls.set_core_dir(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))
        print(f"cls.get_core_dir() = {cls.get_core_dir()}")
        #cls.initialize_startup_project()
    @classmethod
    def initialize_startup_project(cls):
        filename_default_project_entry = "./src/projects/default-project.toml"
        loaded_entry = toml_utils.load_toml(filename_default_project_entry)
        cls.set_project_dir(cls.get_core_dir()+"\\projects\\"+loaded_entry["project_directory"])

    @staticmethod
    def check_file(filepath):
        if not(os.path.isfile(filepath)):
            print(f"The file does not exist: {filepath}")
            #raise RuntimeError("Stopping execution")
            raise SystemExit
        else:
            # the file exists
            return True
        
