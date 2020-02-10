#!/usr/bin/env python

from distutils.core import setup
from setuptools import find_packages

setup(name='low_thru',
      version='0.1',
      description='A package for generating complex file structures'
                  ' intended for low throughputcomputational applications',
      author='Ben Comer',
      author_email='ben.comer@gatech.edu',
      url='https://github.com/medford-group/low_throughput_calcs',
      #scripts=['make_structure'],
      packages=find_packages(),
      install_requires=['numpy']
     )

