import os
from shutil import copy
import yaml
import numpy as np
from itertools import product

from tempfile import mkstemp
from shutil import move
from os import remove, close


def replace(file_path, pattern, subst):
    #Create temp file
    fh, abs_path = mkstemp()
    with open(abs_path,'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                new_file.write(line.replace(pattern, subst))
    close(fh)
    #Remove original file
    remove(file_path)
    #Move new file
    move(abs_path, file_path)


def generate_file_structure(filename):
    structure_dict = yaml.load(open(filename, 'r'))
    if 'variables' in structure_dict:
        variables = structure_dict.pop('variables')
    if 'files' in structure_dict:
        files = structure_dict.pop('files')
    if 'directories' in structure_dict:
        tree = structure_dict['directories']
    recursive_dict_read(tree, variables, files)

def copy_files(files):
    if type(files) != list:
        raise Exception('files must be a list')
    for fil in files:
        filename = fil.split(os.sep)[-1]
        copy(fil, '.')
        replace(filename, 'lol', 'lol')
    
def recursive_dict_read(structure_dict, variables=None, files=None):
    """
    a function to recursively build a file tree
    """
    for key, value in structure_dict.items():
        if variables is not None:
            var_combos = find_var_combos(variables, key)
            #print(var_combos)
            for combo in var_combos:
                os.mkdir(combo)
                os.chdir(combo)
                if type(value) == dict:
                    recursive_dict_read(value, variables)
                os.chdir('..')
        else:
            os.mkdir(key)
            os.chdir(key)
            if type(value) == dict:
                # if we're not at the bottom, keep building
                recursive_dict_read(value, variables)
            else:
                # if we're at the bottom, copy the files
                pass
            
                copy()
            os.chdir('..')

def find_var_combos(variables, name):
    

"""
def find_var_combos(variables, name):
    """
    """
    This function finds all the instances of the variables present in curly
    brackets in the string and returns all the combinations of these variables
    with the values provided in the `variables` argument.

    this is not very efficient
    """
    """
    vars_blocks = []
    vars_present = []
    var_ranges = {a[0]:np.arange(*a[1]) for a in variables.items()}
    tmp_name = name
    evaluated_strings = []
    names = []
    blocks_dict = {}
    prev_name = ''
    if '{' not in name:
        return [name]
    # find all the variable blocks they input
    while True:
        current_block = tmp_name.split('{')[len(tmp_name.split('{')) -1 ].split('}')[0]
        tmp_name = tmp_name.replace('{'+current_block+'}', '')
        if prev_name == tmp_name:
            break
        vars_blocks.append(current_block)
        prev_name = tmp_name
    for var_block in vars_blocks:
        evaluated_strings = []
        tmp_var_block = var_block
        for variable in sorted(list(variables.keys()), key=len):
            if variable in tmp_var_block:
                vars_present.append(variable)
                tmp_var_block.replace(variable,'<>')
        vars_present = sorted(list(set(vars_present)), key=len)
        combos = product(*[var_ranges[a] for a in vars_present])
        for combo in combos:
            string = var_block
            for i, value in enumerate(combo):
                string = string.replace(vars_present[i], str(value))
            evaluated_strings.append(str(eval(string))) # TODO: make this secure
        blocks_dict[var_block] = evaluated_strings.copy()
    for combo in product(*[blocks_dict[a] for a in vars_blocks]):
        string = name
        for i, evaluated_block in enumerate(combo):
            string = string.replace('{' + vars_blocks[i] + '}', evaluated_block)
        names.append(string)
        
            

    #for i, var_block in enumerate(vars_blocks):
    #    combos = 
    #    for variable_combo in sorted(list(variables.keys()), key=len):
    #        for value in var_ranges[variable]:
    #                fo
    #                evaluated_strings.append(var_block.replace(variable, str(value)))
        #for variable in sorted(list(variables.keys()), key=len):
        #    for value in var_ranges[variable]
        #        evaluated_strings.append(var_block.replace(variable, str(value)))
                
    return names 
"""

#def recursive_gen(key):
#    os.mkdir(key)
#    os.chdir(key)
#    if type(value) == dict:
#        recursive_dict_read(value)
#    os.chdir('..')
