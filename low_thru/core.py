import os
import ast
from shutil import copy
import yaml
import numpy as np
from itertools import product

from tempfile import mkstemp
from shutil import move
from os import remove, close

absolute_base_dir = os.getcwd()

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
    # transform the variables into the ranges
    var_ranges = {}
    for name, var in variables.items():
        if [type(a) == str for a in var] == [True] * len(var):
            var_ranges[name] = var
        else:
            var_ranges[name] = np.arange(*var)
    recursive_dict_read(tree, var_ranges, files)

def copy_files(files, variables_dict):
    if files is None:
        return None
    if type(files) != list:
        raise Exception('files must be a list')
    for fil in files:
        orig_filename = fil.split(os.sep)[-1]
        path = fil.split(os.sep)[:-1]
        filename = orig_filename
        for var, value in variables_dict.items():
            if '{' + var + '}' in orig_filename:
                filename = orig_filename.replace('{' + var + '}', str(value))
        if '{' in filename and '}' in filename:
            continue
        # if an absolute path is not given, use the top level directory
        if not fil.startswith('/'):
            new_file =absolute_base_dir + os.sep + fil.replace(orig_filename, filename)
        else:
            new_file = fil.replace(orig_filename, filename)

        copy(new_file, '.')
        for var, value in variables_dict.items():
            replace(filename, '{'+var+'}', str(value))
            
    
def recursive_dict_read(structure_dict, variables=None, files=None,
                        variable_values={}):
    """
    a function to recursively build a file tree
    """
    for key, value in structure_dict.items():
        if variables is not None:
            var_combos, var_values = find_var_combos(variables, key, variable_values)
            #print(var_combos)
            for combo, vals in zip(var_combos, var_values):
                if not os.path.isdir(combo):
                    os.mkdir(combo)
                os.chdir(combo)
                if type(value) == dict:
                    recursive_dict_read(value, variables, files=files, 
                                        variable_values=vals)
                else:
                    # if we're at the bottom, copy the files
                    copy_files(files, vals)

                os.chdir('..')
        else:
            if not os.path.isdir(key):
                os.mkdir(key)
            os.chdir(key)
            if type(value) == dict:
                # if we're not at the bottom, keep building
                recursive_dict_read(value, variables,
                                    variable_values=var_values)
            else:
                # if we're at the bottom, copy the files
                copy_files(files, variable_values)
            
            os.chdir('..')

"""
def find_var_combos(variables, name, variable_values):
    vars_blocks = []
    vars_present = []
    tmp_name = name
    names = []
    prev_name = ''
    variable_values_list = []
    if '{' not in name:
        return [name], [variable_values]
    # find all the variable blocks they input
    while True:
        current_block = tmp_name.split('{')[len(tmp_name.split('{')) -1 ].split('}')[0]
        tmp_name = tmp_name.replace('{'+current_block+'}', '')
        if prev_name == tmp_name:
            break
        vars_present.append(current_block)
        prev_name = tmp_name
    for var in vars_present:
        if var not in variables:
            raise Exception('the variable {} was used, but was not defined'.format(var))
    all_combos = product(*[variables[a] for a in vars_present]) 
    for combo in all_combos:
        tmp_name = name
        for var, value in zip(vars_present, combo):
            tmp_name = tmp_name.replace('{'+var+'}', str(value))
            variable_values[var] = value
        names.append(tmp_name)
        variable_values_list.append(variable_values.copy())
    return names, variable_values_list
"""

def find_var_combos(variables, name, variable_values):
    """
    This function finds all the instances of the variables present in curly
    brackets in the string and returns all the combinations of these variables
    with the values provided in the `variables` argument.

    this is not very efficient
    """
    vars_blocks = []
    vars_present = []
    #var_ranges = {a[0]:np.arange(*a[1]) for a in variables.items()}
    tmp_name = name
    evaluated_strings = []
    names = []
    blocks_dict = {}
    prev_name = ''
    if '{' not in name:
        return [name], [variable_values]
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
        variable_dicts = []
        tmp_var_block = var_block
        for variable in sorted(list(variables.keys()), key=len):
            if variable in tmp_var_block:
                vars_present.append(variable)
                tmp_var_block.replace(variable,'<>')
    vars_present = sorted(list(set(vars_present)), key=len)
    #combos = product(*[variables[a] for a in vars_present])
    for var_block in vars_blocks:
        combos = product(*[variables[a] for a in vars_present])
        evaluated_strings = [] 
        for combo in combos:
            string = var_block
            contains_strings = False
            var_val_dict = {vars_present[i]:value for i, value in enumerate(combo)}
            for var, value in var_val_dict.items():
                if type(value) == str:
                    contains_strings = True
                string = string.replace(var, str(value))
            variable_values.update(var_val_dict)
            variable_dicts.append(variable_values.copy())
            if not contains_strings:
                evaluated_strings.append(str(ast.literal_eval(string))) # TODO: make this secure
            else:
                evaluated_strings.append(str(string))
        blocks_dict[var_block] = evaluated_strings.copy()
    #for combo in product(*[blocks_dict[a] for a in vars_blocks]):
    for combo in zip(*[blocks_dict[a] for a in vars_blocks]):
        string = name
        for i, evaluated_block in enumerate(combo):
            string = string.replace('{' + vars_blocks[i] + '}', evaluated_block)
            
        names.append(string)
 
    return names, variable_dicts







