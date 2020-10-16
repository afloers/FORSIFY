#!/usr/bin/env python
#
# See top-level LICENSE file for Copyright information
#
# -*- coding: utf-8 -*-

import glob
import pandas as pd

import io
import tempfile
import pathlib
import errno
from astropy.io import fits

import pypeit
from pypeit.pypeitsetup import PypeItSetup
from pypeit.spectrographs.util import load_spectrograph
from pypeit.par import pypeitpar
from pypeit import fluxcalibrate

from convert_to_iraf import PypeIt_to_iraf


class FORS_setup:
    def __init__():
        pass

    def reduce(self):
        pass

    def flux_spectra(self):
        pass

    def create_archival_data_symlinks(self):
        pass

    def use_bias_frames(self):
        pass

    def choose_detector_chip(self):
        pass

    def change_flat_type(self):
        pass

    def read_pypeit_sorted(self):
        pass

    def write_virt_pypeit_file(self):
        pass

    def make_pypeit_header(self):
        pass

    def grab_sensfunc(self, grism):
        pass
