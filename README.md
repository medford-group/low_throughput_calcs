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

The directories field should have a yaml tree containing the hierachy of the directory structure. each tab level indicates a movement deeper into the file tree. for example the directory input below would make a directory called `memes` and inside that directory would be two folders: `doge` and `Elon_Musk`.

```
directories:
    memes:
        doge:
        Elon_Musk:
```

## variables

variables contains a set of variables that will be used in the directory tree. You must put this in the format `variable: [varible_start, variable_stop, variable_step_size]` (note that is is using the [numpy arange function](https://docs.scipy.org/doc/numpy/reference/generated/numpy.arange.html) underneath the hood). You may also enter a list of strings which will simply by used as such.

```

```


## Example
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

This file would make a top level directory called "Cu" and inside that would be directories 
