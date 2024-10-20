import os
import time
import warnings
from slurmtools.slurmsh import SlurmSh
from ase.calculators.genericfileio import GenericFileIOCalculator
from ase.calculators.espresso import EspressoProfile,EspressoTemplate


def tail(fn, n):
    """ファイルを開いてすべての行をリストで取得する"""
    with open(fn, 'r') as f:
        f.readline()
        lines = f.readlines()
    return lines[-n:]

def lineisin(fn):
    with open(fn, 'r') as f:
        lines = f.readlines()
    return bool(len(lines))

def waitqe(checkinterval=5):
    '''Wait for the completion of the calculation'''
    
    file_name_output = "espresso.pwo"
    file_name_error = "espresso.err"
    COMPLETED=[
        '=------------------------------------------------------------------------------=\n',
        '   JOB DONE.\n',
        '=------------------------------------------------------------------------------=\n'
        ]
    while True:
        time.sleep(checkinterval)
        if lineisin(file_name_error):
            print("Error detected in espresso.err")
            break
        if tail(file_name_output, 3) == COMPLETED:
            print("Job completed successfully")
            break
        

class BatchEspressoProfile(EspressoProfile):
    """
    ASEのEspressoProfileを継承し、SlurmShオブジェクトを追加.
    """
    def __init__(self, command, pseudo_dir, slshobj:SlurmSh, **kwargs):
        super().__init__(command, pseudo_dir, **kwargs)
        self.slshobj = slshobj
        
        
class BatchEspressoTemplate(EspressoTemplate):
    '''EspressoTemplateを継承し、executeメソッドをbatch処理に対応するよう上書き'''
    def batchexecute(self, directory, slshobj:SlurmSh):
        directory=slshobj.dir
        with open(os.path.join(directory, 'espresso.pwo'), mode='w') as f:
            f.write("")
        with open(os.path.join(directory, 'espresso.err'), mode='w') as f:
            f.write("")
            
        slshobj.submit_sh()
        #cmd='sbatch /home/b/b38622/research/ASE_batch/qebatch.sh'
        #check_call(cmd.split())
        
        waitqe(checkinterval=5)
        
    def execute(self, directory, profile):
        self.batchexecute(directory, profile.slshobj)
        
        

        
compatibility_msg = (
    'Espresso calculator is being restructured.  Please use e.g. '
    "Espresso(profile=EspressoProfile(argv=['mpiexec', 'pw.x'])) "
    'to customize command-line arguments.'
)

class BatchEspresso(GenericFileIOCalculator):
    def __init__(
        self,
        *,
        profile:BatchEspressoProfile,
        command=GenericFileIOCalculator._deprecated,
        label=GenericFileIOCalculator._deprecated,
        directory='.',
        **kwargs,
    ):
        """
        All options for pw.x are copied verbatim to the input file, and put
        into the correct section. Use ``input_data`` for parameters that are
        already in a dict.

        input_data: dict
            A flat or nested dictionary with input parameters for pw.x
        pseudopotentials: dict
            A filename for each atomic species, e.g.
            ``{'O': 'O.pbe-rrkjus.UPF', 'H': 'H.pbe-rrkjus.UPF'}``.
            A dummy name will be used if none are given.
        kspacing: float
            Generate a grid of k-points with this as the minimum distance,
            in A^-1 between them in reciprocal space. If set to None, kpts
            will be used instead.
        kpts: (int, int, int), dict, or BandPath
            If kpts is a tuple (or list) of 3 integers, it is interpreted
            as the dimensions of a Monkhorst-Pack grid.
            If ``kpts`` is set to ``None``, only the Γ-point will be included
            and QE will use routines optimized for Γ-point-only calculations.
            Compared to Γ-point-only calculations without this optimization
            (i.e. with ``kpts=(1, 1, 1)``), the memory and CPU requirements
            are typically reduced by half.
            If kpts is a dict, it will either be interpreted as a path
            in the Brillouin zone (*) if it contains the 'path' keyword,
            otherwise it is converted to a Monkhorst-Pack grid (**).
            (*) see ase.dft.kpoints.bandpath
            (**) see ase.calculators.calculator.kpts2sizeandoffsets
        koffset: (int, int, int)
            Offset of kpoints in each direction. Must be 0 (no offset) or
            1 (half grid offset). Setting to True is equivalent to (1, 1, 1).

        """

        if command is not self._deprecated:
            raise RuntimeError(compatibility_msg)

        if label is not self._deprecated:
            warnings.warn(
                'Ignoring label, please use directory instead', FutureWarning
            )

        if 'ASE_ESPRESSO_COMMAND' in os.environ and profile is None:
            warnings.warn(compatibility_msg, FutureWarning)

        directory=profile.slshobj.dir
        template = BatchEspressoTemplate()
        
        super().__init__(
            profile=profile,
            template=template,
            directory=directory,
            parameters=kwargs,
        )
