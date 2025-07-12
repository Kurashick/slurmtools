from hpctools.jobmanegementtool import SchedulerJob
from ase.calculators.openmx import OpenMX

class BatchOpenMX(OpenMX):
    """
    A class to run OpenMX calculations on a scheduler like Slurm.
    """
    def __init__(self, label='ase', directory='./openmx',
                 checkinterval=5,
                 job:SchedulerJob=None,**kwargs):
        command="openmx"
        self.checkinterval = checkinterval
        self.job = job
        super().__init__(label=label, directory=directory,command=command, **kwargs)
        
    def run(self):
        run = self.run_on_scheduler
        run()
        
    def run_on_scheduler(self):
        """
        Execute the OpenMX using Slurm Batch System. In order to use this,
        Your system should have Scheduler. 
        """  
        self.job.submit_job(wait=True,checkinterval=self.checkinterval)