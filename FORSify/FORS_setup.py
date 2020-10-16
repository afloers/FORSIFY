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
        sorted_file = glob.glob(self.working_dir + "/*.sorted")[0]
        df = pd.read_table(sorted_file, sep="|", header=13, skipinitialspace=True,)
        df.drop(df.tail(1).index, inplace=True)  # remove unused last row
        df = df.drop(df.columns[0], axis=1)  # remove empty col due to pipe
        df = df.drop(df.columns[-1], axis=1)  # remove empty col due to pipe
        a = df.columns
        df.columns = [a[i].strip() for i in range(len(a))]
        self.sorted = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

    def write_virt_pypeit_file(self):
        modified_df = self.sorted.copy()
        modified_df[" "] = " "
        modified_df["  "] = "  "
        modified_df = modified_df.set_index("  ")
        self.virt_file = io.StringIO()
        modified_df.to_csv(self.virt_file, sep="|")
        content = self.virt_file.getvalue().replace("|", " | ")
        self.virt_file = io.StringIO()
        self.make_pypeit_header()
        self.virt_file.write(self.pypeit_header)
        self.virt_file.write(content)
        self.virt_file.write("data end\n")
        self.tmp = tempfile.NamedTemporaryFile()
        with open(self.tmp.name, "w") as f:
            f.write(self.virt_file.getvalue())
        with open(os.path.join(self.working_dir, "FORSify.pypeit"), "w") as f:
            f.write(self.virt_file.getvalue())

    def make_pypeit_header(self):
        pass

    def grab_sensfunc(self, grism):
        pass
