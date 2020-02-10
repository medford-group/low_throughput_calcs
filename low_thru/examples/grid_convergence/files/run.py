from ase.io import read
from sparc.sparc_core import SPARC
import json

parameters = json.load(open('parameters.json','r'))

parameters['BC'] = [True] * 3

parameters['h'] = {h}
parameters['EXCHANGE_CORRELATION'] = 'LDA_PZ'

atoms = read('structure.xyz')
atoms.center()
calc = SPARC(**parameters)
atoms.set_calculator(calc)
eng = atoms.get_potential_energy()

with open('energy.txt', 'w') as f:
    f.write(str(eng))

