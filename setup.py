# !usr/bin/env python
# -*- coding: utf-8 -*-
#
# Licensed under a 3-clause BSD license.

import sys
import os
import glob

from setuptools import setup, find_packages

from extension_helpers import get_extensions


def get_data_files():
    """ Build the list of data files to include.  """
    data_files = []

    # Walk through the data directory, adding all files
    data_generator = os.walk("FORSify/data")
    for path, directories, files in data_generator:
        for f in files:
            data_path = "/".join(path.split("/")[1:])
            data_files.append(os.path.join(data_path, f))

    # Add pipeline and spectrograph settings
    settings = glob.glob("pypeit/settings/settings.*")
    settings = ["/".join(path.split("/")[1:]) for path in settings]
    data_files.extend(settings)

    return data_files


def get_scripts():
    """ Grab all the scripts in the bin directory.  """
    scripts = []
    if os.path.isdir("bin"):
        scripts = [
            fname
            for fname in glob.glob(os.path.join("bin", "*"))
            if not os.path.basename(fname).endswith(".rst")
        ]
    return scripts


def get_requirements():
    """ Get the requirements from a system file.  """
    name = "FORSify/requirements.txt"

    requirements_file = os.path.join(os.path.dirname(__file__), name)
    install_requires = [
        line.strip().replace("==", ">=")
        for line in open(requirements_file)
        if not line.strip().startswith("#") and line.strip() != ""
    ]
    return install_requires


NAME = "FORSify"
# do not use x.x.x-dev.  things complain.  instead use x.x.xdev
VERSION = "0.1.0"
entry_points = {}


def run_setup(data_files, scripts, packages, install_requires):

    # TODO: Are any/all of the *'d keyword arguments needed? I.e., what
    # are the default values?

    setup(
        name=NAME,
        provides=NAME,  # *
        version=VERSION,
        license="MIT",
        description="Automatic ESO VLT FORS2 Data Reduction Pipeline",
        long_description=open("README.md").read(),
        author="A. Floers",
        author_email="floersandreas@gmail.com",
        keywords="ESO VLT FORS2 automatic pipeline",
        url="https://github.com/afloers/FORSIFY",
        packages=packages,
        package_data={"pypeit": data_files, "": ["*.rst", "*.txt"]},
        python_requires=">=3.7",
        include_package_data=True,
        scripts=scripts,
        install_requires=install_requires,
        requires=["Python (>3.7.0)"],  # *
        zip_safe=False,  # *
        use_2to3=False,  # *
        setup_requires=["pytest-runner"],
        tests_require=["pytest"],
        ext_modules=get_extensions(),
        entry_points=entry_points,
        classifiers=["Topic :: Scientific/Engineering :: Astronomy",],
    )


# -----------------------------------------------------------------------
if __name__ == "__main__":

    # Compile the data files to include
    data_files = get_data_files()
    # Compile the scripts in the bin/ directory
    scripts = get_scripts()
    print(scripts)
    # Get the packages to include
    packages = find_packages()
    # Collate the dependencies based on the system text file
    install_requires = get_requirements()
    install_requires = []  # Remove this line to enforce actual installation
    # Run setup from setuptools
    run_setup(data_files, scripts, packages, install_requires)


# #!/usr/bin/env python
#
# from setuptools import setup
# from os import path
#
# here = path.abspath(path.dirname(__file__))
#
# # Get the long description from the README file
# with open(path.join(here, "README.md"), encoding="utf-8") as f:
#     long_description = f.read()
#
# KEYWORDS = """\
# ESO
# data
# reduction
# FORS2
# pipeline
# physics
# python
# """
# CLASSIFIERS = """\
# Development Status :: 3 - Alpha
# Intended Audience :: Science/Research
# License :: MIT License
# Operating System :: MacOS :: MacOS X
# Operating System :: POSIX :: Linux
# Programming Language :: Python
# Programming Language :: Python :: 3
# Programming Language :: Python :: 3.6
# Programming Language :: Python :: 3.7
# Programming Language :: Python :: 3.8
# Topic :: Scientific/Engineering
# Topic :: Scientific/Engineering :: Physics
# """
#
# setup(
#     name="FORSify",
#     version="0.1.0",
#     description="Automatic Data Reduction Pipeline",
#     long_description=long_description,
#     long_description_content_type="text/markdown",
#     url="https://github.com/afloers/FORSIFY",
#     author="A. Floers",
#     author_email="floersandreas@gmail.com",
#     license="MIT",
#     classifiers=CLASSIFIERS.strip().split("\n"),
#     keywords=KEYWORDS.strip().replace("\n", " "),
#     extras_require={"test": ["pytest", "pytest-cov"],},
#     packages=["FORSify",],
# )
