#!/usr/bin/env python

from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

KEYWORDS = """\
ESO
data
reduction
FORS2
pipeline
physics
python
"""
CLASSIFIERS = """\
Development Status :: 3 - Alpha
Intended Audience :: Science/Research
License :: MIT License
Operating System :: MacOS :: MacOS X
Operating System :: POSIX :: Linux
Programming Language :: Python
Programming Language :: Python :: 3
Programming Language :: Python :: 3.6
Programming Language :: Python :: 3.7
Programming Language :: Python :: 3.8
Topic :: Scientific/Engineering
Topic :: Scientific/Engineering :: Physics
"""

setup(
    name="FORSify",
    version="0.1.0",
    description="Automatic Data Reduction Pipeline",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/afloers/FORSIFY",
    author="A. Floers",
    author_email="floersandreas@gmail.com",
    license="MIT",
    classifiers=CLASSIFIERS.strip().split("\n"),
    keywords=KEYWORDS.strip().replace("\n", " "),
    extras_require={"test": ["pytest", "pytest-cov"],},
    packages=["FORSify",],
)
