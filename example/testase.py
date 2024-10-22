import os
import json
from ase.build import fcc111
from slurmtools.slurmsh import SlurmSh
from slurmtools.batchespresso import BatchEspressoProfile, BatchEspresso

os.chdir('/home/b/b38622/develop/slurmtools/example')
currentdir = os.getcwd()


ppjson = open('/home/b/b38622/research/qe/SSSP_1.3.0_PBE_efficiency.json','r')
pps = json.load(ppjson)


def pp(Atom_names:list)->dict:
    pseudodict={}
    for Atom_name in Atom_names:
        pseudodict[Atom_name]=pps[Atom_name]['filename']
    return pseudodict

def setcalc():
    pseudopotentials = pp(['Ag','C'])
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
    obj.set_batch(p="gr10569b",t="24:00:00",rsc='p=108:t=1:c=1:m=4G',o='output/%x.%j.out',e='output/%x.%j.err')
    obj.set_command('srun pw.x -nk 3 -nt 6 -nd 6 < ./espresso.pwi > ./espresso.pwo')
    # Optionally create profile to override paths in ASE configuration:
    profile = BatchEspressoProfile(
        pseudo_dir='/home/b/b38622/research/qe/pseudo',
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




import traceback

slab = fcc111('Ag', size=(2, 2, 2), vacuum=10.0)

try:
    slab.calc = setcalc()
    e="Energy:"+str(slab.get_potential_energy())  # This will run a single point calculation
    file_name = "/home/b/b38622/develop/slurmtools/example/testase.txt"
    # openしたファイルをfとして、字下げした処理を行う
    with open(file_name, mode="w") as f:
        f.write(e)
except Exception as p:
    e = list(traceback.TracebackException.from_exception(p).format())
    file_name = "/home/b/b38622/develop/slurmtools/example/testase.txt"
    with open(file_name, mode='w') as f:
        f.write('\n'.join(e))




