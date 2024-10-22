import os
from ase.build import fcc111
from slurmtools.slurmsh import SlurmSh
from slurmtools.batchespresso import BatchEspressoProfile, BatchEspresso

os.chdir('path/to/example')
currentdir = os.getcwd()


def setcalc():
    pseudopotentials = {'Ag': 'Ag_ONCV_PBE-1.0.oncvpsp.upf'}
    input_data = {
        'system': {
            'ecutwfc': 60, 
            'ecutrho': 480,
            'occupations':'smearing', 
            'smearing':'mp', 
            'degauss':0.06
        },
        'disk_io': 'low',  # Automatically put into the 'control' section
    }
    obj=SlurmSh(dir=currentdir,filename='qebatch')
    obj.set_batch(p="gr19999b",t="24:00:00",rsc='p=108:t=1:c=1:m=4G',o='output/%x.%j.out',e='output/%x.%j.err')
    obj.set_command('srun pw.x -nk 3 -nt 6 -nd 6 < ./espresso.pwi > ./espresso.pwo')
    # Optionally create profile to override paths in ASE configuration:
    profile = BatchEspressoProfile(
        pseudo_dir='path/to/pseudo',
        slshobj=obj
    )
    
    calc = BatchEspresso(
        profile=profile, 
        pseudopotentials=pseudopotentials, 
        tstress=True,  # deprecated, put in input_data
        tprnfor=True,  # deprecated, put in input_data
        input_data=input_data,
        kpts=(1, 1, 1)
    )

    return calc


# Create a slab and set the calculator
slab = fcc111('Ag', size=(2, 2, 2), vacuum=10.0)
slab.calc = setcalc()

# Run a single point calculation
e="Energy:"+str(slab.get_potential_energy()) 
file_name = "path/to/example/testase.txt"
with open(file_name, mode="w") as f:
    f.write(e)
    