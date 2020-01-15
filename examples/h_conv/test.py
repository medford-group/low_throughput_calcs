from low_thru.core import recursive_dict_read, generate_file_structure
import yaml

#structure_dict = yaml.load(open('structure.yaml', 'r'))

#recursive_dict_read(structure_dict)

generate_file_structure('structure.yaml')
