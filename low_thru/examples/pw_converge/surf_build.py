from ase.build import surface, fcc100, add_adsorbate
from ase.constraints import FixAtoms
from ase.io import read
import numpy as np
from ase.visualize import view

#bulk = read('../bulk/converged_bulk.traj')
#a=3.89
#a = np.linalg.norm(bulk.cell[0])

vac = 6

#atoms = fcc100('Pd', (2,2,4), a=a, vacuum=10)
atoms = fcc100('Pd', (2,2,{l}), vacuum=vac)
c = FixAtoms(mask=[a.z < vac+2 for a in atoms])
atoms.set_constraint(c)
#atoms *= (2,2,1)

atoms.write('structure.traj')
