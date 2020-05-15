#!/usr/bin/env python3

from setuptools import setup, find_packages
setup(
    name="Enigne",
    version="0.1",
    packages=find_packages(),
    scripts=['bin/enigne-perft'],
    tests_require=['pytest', 'pytest-console-scripts'],
)
