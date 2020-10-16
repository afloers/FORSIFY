#!/usr/bin/env python
#
# See top-level LICENSE file for Copyright information
#
# -*- coding: utf-8 -*-

import glob
import pandas as pd
import argparse
import os
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


def parse_args():
    argparser = argparse.ArgumentParser(description="Script for running FORSify")
    group = argparser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-r", "--root", type=str, default=None, help="Raw data directory"
    )

    argparser.add_argument(
        "-c",
        "--chip",
        default=1,
        type=int,
        choices=[1, 2],
        help="FORS detector ccd number; can be [1,2].",
    )
    argparser.add_argument(
        "-b",
        "--bias",
        default=True,
        type=bool,
        help="Specifies whether bias frames are used or not. The default is True.",
    )
    argparser.add_argument(
        "-f",
        "--flat",
        default=["illumflat", "pixelflat", "trace"],
        help='File type of flat field images. Can be any combination of ["illumflat", "pixelflat", "trace"]',
    )
    argparser.add_argument(
        "-s",
        "--sources",
        default=0,
        type=int,
        help="Maximum number of sources to model/extract. An arbitrary number of sources can be specified with '0'.",
    )
    argparser.add_argument(
        "-v",
        "--verbosity",
        type=int,
        default=2,
        help="Verbosity level between 0 [none] and 2 [all]",
    )
    argparser.add_argument(
        "-o",
        "--overwrite",
        default=True,
        action="store_true",
        help="Overwrite any existing files/directories",
    )
    argparser.add_argument(
        "-a",
        "--archival",
        default=False,
        action="store_true",
        help="If True, use archival calibration data instead.",
    )
    return argparser.parse_args()


def main(args):
    pass
