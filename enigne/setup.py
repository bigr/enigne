#!/usr/bin/env python3
import os
from setuptools import setup, find_packages

about = {}
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "enigne", "__about__.py")) as fp:
    exec(fp.read(), about)

setup(
    name=about['__name__'],
    version=about['__version__'],
    author=about['__author__'],
    packages=find_packages(),
    scripts=['bin/enigne-perft', 'bin/enigne'],
    tests_require=['pytest', 'pytest-console-scripts'],
)
