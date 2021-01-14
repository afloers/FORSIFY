# FORSify - automatic data reduction of ESO VLT / FORS2 observations



# Requirements

(see `FORSify/requirements.txt`)

* python
* numpy
* scipy
* pandas
* matplotlib
* astropy
* ginga
* h5py
* future
* PyYAML
* linetools
* IPython
* scikit-learn
* configobj
* pypeit

# Installation instructions
You can install the necessary packages and the pipeline by running
the following commands in your terminal:
```
git clone https://github.com/afloers/FORSIFY.git
cd FORSify
conda env create -n forsify --file FORSify/requirements.txt
conda activate forsify
pip install spectres
python setup.py install
```

Then, install spectres manually:
```console
foo@bar:~$ pip install spectres
```

# Usage
See all FORSify options by running the following command in your terminal:
```console
foo@bar:~$ FORSify -h
usage: FORSify [-h] -r ROOT [-c {1,2}] [-b BIAS] [-f FLAT] [-s SOURCES] [-v VERBOSITY] [-o] [-a]

Script for running FORSify

optional arguments:
  -h, --help            show this help message and exit
  -r ROOT, --root ROOT  Raw data directory
  -c {1,2}, --chip {1,2}
                        FORS detector ccd number; can be [1,2].
  -b BIAS, --bias BIAS  Specifies whether bias frames are used or not. The default is True.
  -f FLAT, --flat FLAT  File type of flat field images. Can be any combination of ["illumflat", "pixelflat", "trace"]
  -s SOURCES, --sources SOURCES
                        Maximum number of sources to model/extract. An arbitrary number of sources can be specified with '0'.
  -v VERBOSITY, --verbosity VERBOSITY
                        Verbosity level between 0 [none] and 2 [all]
  -o, --overwrite       Overwrite any existing files/directories
  -a, --archival        If True, use archival calibration data instead.
```
For standard reductions, only two options are important:

`-r` indicates the raw data folder with respect to your current working directory.

If `--archival` is set the pipeline uses archival calibration frames for the reduction. In this case, only the science frame needs to be placed in the raw data folder.

# Output
FORSify reduces and fluxes the science frames automatically. Fluxing is performed using a sensitivity function created from all standard stars of the corresponding semester using the same setup as the science frame.

Output files are given both in the pypeit and iraf format. Iraf output files are given in the `Output` directory, whereas pypeit output files are found in the standard `Science` directory.

# License (MIT)

(see `LICENSE`)

MIT License

Copyright (c) 2020 Andreas Flörs

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
