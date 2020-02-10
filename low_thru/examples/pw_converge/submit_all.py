import os
from subprocess import call
import sys

cur_dir=os.path.realpath(".")
import os
for root, dirs, files in os.walk(".", topdown=False):
    for name in files:
        if name == 'run.sh':
            os.chdir(os.path.join(root))
            call(["qsub","run.sh"])
            os.chdir(cur_dir)
 
        
        
