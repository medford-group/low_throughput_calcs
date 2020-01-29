from ase.build import molecule
from ase.constraints import FixAtoms
from ase.io import read
import numpy as np
from ase.visualize import view

#bulk = read('../bulk/converged_bulk.traj')
#a=3.89
#a = np.linalg.norm(bulk.cell[0])

vac = 20


atoms = read('nitrate.xyz')

atoms.write('structure.traj')
