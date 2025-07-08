from abc import ABC, abstractmethod
from datetime import datetime as dt
import os

class JobScriptManager(ABC):
    """
    Abstract base class for managing job scripts for HPC job schedulers.
    """
    def __init__(self, dir, script_name):
        self.options = ["#!/bin/bash\n#============ Options ==========="]
        self.command = ["\n#============ Commands ============"]
        self.dir = dir
        self.script_name = script_name


    @abstractmethod
    def set_options(self, **kwargs):
        """
        Set job options.
        kwargs should contain key-value pairs for job options.
        """
        pass
    
    @abstractmethod
    def set_command(self, *commands):
        """
        Set commands to be executed in the job script.
        Multiple commands can be provided as separate arguments.
        """
        pass
    
    def make_scriptfile(self):
        """
        Combine options and commands into a complete script.
        Writes the script to a file.
        """
        script_content = self.options + self.command
        comment = f"\n# made by {self.__class__.__name__} automatically\n# {str(dt.now())}"
        script_content.append(comment)

        self.script_path = os.path.join(self.dir, self.script_name + '.sh')
        with open(self.script_path, mode='w') as f:
            f.write('\n'.join(script_content))
        return
    
    @abstractmethod
    def isRunning(self):
        """
        Check submitted job is still Running
        """
        pass
    
    @abstractmethod
    def quit(self):
        """
        Cancel the job if it is running.
        """
        pass
    
    @abstractmethod
    def wait():
        """
        Wait for the job to complete.
        Returns True if the job completed successfully, False otherwise.
        """
        pass
    
    @abstractmethod
    def submit(self, wait=False, checkinterval=5):
        """
        Submit the job script to the job scheduler.
        Returns the job ID if successful.
        """
        pass
    
    @abstractmethod
    def get_exit_stutus(self):
        """
        Get the exit status of the job.
        Returns True if the job completed successfully, False otherwise.
        """
        pass
    