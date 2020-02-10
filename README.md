# Low Thru

Low Thru is a package for rapidly generating file structures and copying files into those structures. Low Thru is designed to be as simple as possible, generating the desired directory structures and modifying values in the copied files, no more, no less.


## Installation

this package is not on pip yet (and may have serious issues) but may be installed directly from github:

```
pip install git+https://github.com/medford-group/low_throughput_calcs
```

note that you may need a `--user` flag if you are on a supercomputing cluster

## Usage

Low Thru required a structured input file to operate. This input file must be named `structure.yaml`. This file must be in the [yaml](https://learn.getgrav.org/16/advanced/yaml) format and contain three fileds at the top level: `directories`, `variables`, and `files`. An example file can be found below in the examples section.

### Directories

The directories field should have a yaml tree containing the hierachy of the directory structure. each tab level indicates a movement deeper into the file tree. for example the directory input below would make a directory called `stuff` and inside that directory would be two folders: `dogs` and `cars`.

```
directories:
    stuff:
        dogs:
        cars:
```

## variables

variables contains a set of variables that will be used in the directory tree. You must put this in the format `variable: [varible_start, variable_stop, variable_step_size]` (note that is is using the [numpy arange function](https://docs.scipy.org/doc/numpy/reference/generated/numpy.arange.html) underneath the hood). You may also enter a list of strings which will simply by used as such. building on the example above, the structure below will generate 4 additional folders, `1_coins`-`4_coins`.

```
directories:
    stuff:
        dogs:
        cars:
        {b}_coins:
variables:
    - b: [1,5,1]

```

## files

You can speficy files to be copied into the bottom level of each folder. These are contained in the `files` section. These files may be specified using relative paths or absolute paths. The system will also scan each file for instances of the variables you placed further up in the tree (for example {b} above) and replace the variables it finds with the value it has taken on further up in the tree. In the example below, the system will copy the `stuff.txt` file into each of the folders `dogs`, `cars`, etc... for the `{b}_coins` folders, it will scan `stuff.txt` for instances of the string '{b}' and replace them with the variable value in used to generate the folder.

```
directories:
    stuff:
        dogs:
        cars:
        {b}_coins:
variables:
    - b: [1,5,1]

files:
    - stuff.txt

```

## Rules

this list may be incomplete but:

1. you may only specify a variable once in a a given tree


## Full Example
```
directories:
    Cu:
        FD_Grid_{n}_{n}_{n}:
            npts:
            kpts{m}x{m}x1:
                run_{x}:
variables:
    n: [4, 12, 2]
    m: [1, 5, 1]
    x: ['high', 'low']
files:
    - run.sh
    - run.py

```

This file would make a top level directory called "Cu" and inside that would be directories FD\_GRID\_4\_4\_4 through FD\_GRID\_10\_10\_10 at increments of 2. inside each of these is a folder called npts and kpts1\_1\_1 through kpts4\_4\_1 at increments of 1. Inside these are folders named run\_high and run\_low. The files run.sh and run.py in the current direcotry will be copied into all the run\_high and run\_low folders, as well as the npts folders. These files will be scanned for the presence of the variable identifiers {n}, {m}, and {x}. These will be replaced with the values they have taken on in the tree above. Note that the copied of these files in the npts folders will only be scanned for {n} identiers, as the other variables are not defined anywhere in the tree above it.

