from ase.io import read
from ase.optimize import BFGSLineSearch
from espresso import espresso
import numpy as np
import json


parameters = {"xc": "BEEF-vdW", "kpts": [8, 8, 8], "pw": 800.0, "dw": 8000.0, "spinpol": false, "beefensemble": true, "printensemble": true, "convergence": {"energy": 1e-06, "mixing": 0.2, "maxsteps": 1000, "diag": "david"}, "startingwfc": "atomic", "dipole": {"status": false}, "outdir": "esp.log"}
atoms = molecule()

parameters['pw'] = {pw}
parameters['kpts'] = ({kpts}, {kpts}, 1)

atoms = read('structure.traj')
calc = espresso(**parameters)
atoms.set_calculator(calc)

relax = BFGSLineSearch(atoms)
relax.run(fmax=0.05)

eng = atoms.get_potential_energy()

with open('energy.txt', 'w') as f:
    f.write(str(eng))

