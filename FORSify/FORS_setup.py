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
    def __init__(
        self,
        working_dir,
        data_dir,
        chip=1,
        flat=["illumflat", "pixelflat", "trace"],
        bias=True,
        sources=0,
        archival=False,
    ):
        self.working_dir = working_dir
        self.chip = args.chip
        self.flat = args.flat
        self.bias = args.bias
        self.data_dir = args.root
        self.sources = args.sources
        self.archival = args.archival
        self.sorted = None
        self.FORSIfy_path = pathlib.Path(__file__).parent.absolute()

    def reduce(self):
        pass

    def flux_spectra(self):
        pass

    def create_archival_data_symlinks(self):
        pass

    def change_flat_type(self):
        flat_type = ",".join(self.flat)
        self.sorted["frametype"] = self.sorted["frametype"].replace(
            ["pixelflat,trace"], flat_type
        )

    def choose_detector_chip(self):
        chip = "CHIP" + str(self.chip)
        self.sorted = self.sorted.loc[self.sorted["detector"] == chip]

    def use_bias_frames(self):
        if self.bias == False:
            self.sorted = self.sorted.loc[self.sorted["frametype"] != "bias"]

    def read_pypeit_sorted(self):
        pass

    def write_virt_pypeit_file(self):
        pass

    def make_pypeit_header(self):
        pass

    def grab_sensfunc(self, grism):
        pass
