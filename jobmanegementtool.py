from abc import ABC, abstractmethod
from datetime import datetime as dt
import os
import json

class SchedulerJob(ABC):
    """
    Abstract base class for managing job scripts for HPC job schedulers.
    """
    def __init__(self, dir, script_name):
        self.options = ["#!/bin/bash\n#============ Options ==========="]
        self.command = ["\n#============ Commands ============"]
        self.dir = dir
        self.script_name = script_name
        self.script_path = os.path.join(self.dir, self.script_name + '.sh')

    @property
    @abstractmethod
    def option_prefix(self):
        pass
    
    def set_options(self,options):
        """
        Set job options.
        kwargs should contain key-value pairs for job options.
        The prefix argument is used to specify the command prefix (e.g., "#SBATCH").
        """
        for option in options:
            if isinstance(option, str):
                self.options.append(f"{self.option_prefix} {option}")
            else:
                raise ValueError(f"Each option must be provided as a string variable, not {type(option)}.")
    

    def set_command(self, commands):
        """
        Set commands to be executed in the job script.
        Multiple commands can be provided as separate arguments.
        """
        for command in commands:
            if isinstance(command, str):
                self.command.append(command)
            else:
                raise ValueError("Commands must be provided as strings.")
    
    def make_scriptfile(self):
        """
        Combine options and commands into a complete script.
        Writes the script to a file.
        """
        script_content = self.options + self.command
        comment = f"\n# made by {self.__class__.__name__} automatically\n# {str(dt.now())}"
        script_content.append(comment)

        with open(self.script_path, mode='w') as f:
            f.write('\n'.join(script_content))
        return
    
    def export_setting_to_json(self, filename):
        """
        Export the job script settings to a JSON file.
        """
        script_dict = {
            "options": self.options,
            "commands": self.command,
            "script_path": self.script_path
        }
        with open(filename, 'w') as f:
            json.dump(script_dict, f, indent=4)
    
    @abstractmethod
    def isRunning(self):
        """
        Check submitted job is still Running
        """
        pass
    
    @abstractmethod
    def quit_job(self):
        """
        Cancel the job if it is running.
        """
        pass
    
    @abstractmethod
    def wait_job(self):
        """
        Wait for the job to complete.
        Returns True if the job completed successfully, False otherwise.
        """
        pass
    
    @abstractmethod
    def submit_job(self, wait=False, checkinterval=5):
        """
        Submit the job script to the job scheduler.
        Returns the job ID if successful.
        """
        pass
    
    @abstractmethod
    def get_exit_status(self):
        """
        Get the exit status of the job.
        Returns True if the job completed successfully, False otherwise.
        """
        pass
    