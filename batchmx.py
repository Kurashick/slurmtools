import os
from slurmtools.slurmsh import SlurmSh
from ase.calculators.openmx import OpenMX

class BatchOpenMX(OpenMX):
    """
    ASEのOpenMXを継承し、SlurmShオブジェクトを追加.
    commandはSlurmShオブジェクトに移行
    引数にSlurmShオブジェクトを追加
    """
    def __init__(self, label='ase', directory='./openmx',
                 checkinterval=5,
                 slshobj:SlurmSh=None,**kwargs):
        command="openmx"
        self.checkinterval = checkinterval
        self.slshobj = slshobj
        super().__init__(label=label, directory=directory,command=command, **kwargs)
        
    def run(self):
        run = self.run_slurm
        run()
        
    def run_slurm(self):
        """
        Execute the OpenMX using Slurm Batch System. In order to use this,
        Your system should have Scheduler. 
        """
        
        slshobj = self.slshobj
        directory=slshobj.dir
        # 空にしておく必要がある! これがないと、前回の計算結果が残ってしまう
        # 出力ファイルを確認すること！
        #with open(os.path.join(directory, self.label+'.dat'), mode='w') as f:
            #f.write("")
        #with open(os.path.join(directory, self.label+'.log'), mode='w') as f:
            #f.write("")
            
            
        slshobj.submit_sh(wait=True,checkinterval=self.checkinterval)