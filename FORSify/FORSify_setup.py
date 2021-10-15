#!/usr/bin/env python
#
# See top-level LICENSE file for Copyright information
#
# -*- coding: utf-8 -*-

import glob
import pandas as pd
from pkg_resources import resource_filename
import io
import tempfile
import pathlib
from astropy.io import fits
import os
import pypeit
from pypeit.pypeitsetup import PypeItSetup
from pypeit import pypeit
from pypeit.spectrographs.util import load_spectrograph
from pypeit.par import pypeitpar
from pypeit import fluxcalibrate
from FORSify.util import PypeIt_to_iraf
from FORSify.util import symlink_force


class FORS_setup:
    def __init__(self, working_dir, args):
        self.working_dir = working_dir
        self.args = args
        self.chip = args.chip
        self.flat = args.flat
        self.bias = args.bias
        self.data_dir = args.root
        self.sources = args.sources
        self.archival = args.archival
        self.sorted = None
        self.masters = args.masters

        # self.FORSIfy_path = resource_filename("FORSify")
        self.FORSIfy_path = pathlib.Path(__file__).parent.absolute()

    def reduce(self):
        if self.archival == True:
            print("Using archival data")
            grism = self.get_correct_grism()
            print(grism)
            self.create_archival_data_symlinks(grism)
            if self.masters == True:
                self.copy_archival_masters(grism)
        if self.args.root is not None:
            ps = PypeItSetup.from_file_root(
                self.args.root,
                "vlt_fors2",
                extension=".fits",
                output_path=self.working_dir,
            )
        else:
            raise IOError("Need to set -r!")
        ps.run(setup_only=True, sort_dir=self.working_dir, write_bkg_pairs=False)
        self.read_pypeit_sorted()
        self.change_flat_type()
        self.choose_detector_chip()
        self.use_bias_frames()
        print(self.sorted)
        self.write_virt_pypeit_file()
        pipeline = pypeit.PypeIt(
            self.tmp.name,
            verbosity=self.args.verbosity,
            reuse_masters=self.masters,
            overwrite=self.args.overwrite,
        )
        pipeline.reduce_all()
        self.flux_spectra()

    def get_correct_grism(self):
        raw_dir = os.path.join(self.args.root, "*.fits")
        file = glob.glob(raw_dir)[0]
        header = fits.open(file)[0].header
        grism = header["HIERARCH ESO INS GRIS1 NAME"]
        return grism

    def flux_spectra(self):
        science_dir = os.path.join(os.path.split(self.working_dir)[0], "Science")
        spec1dfiles = glob.glob(science_dir + "/spec1d*.fits")
        sensfiles = []
        objects = self.sorted.loc[
            self.sorted["frametype"].isin(["standard", "science"])
        ]
        self.objectfiles = objects["filename"].values
        self.corresponding_files = {}
        for idx, file in enumerate(spec1dfiles):
            found = False
            for jdx, objectfile in enumerate(self.objectfiles):
                if objectfile[:-5] in file:
                    self.corresponding_files[file] = objectfile
                    found = True
                    break
            if found == False:
                spec1dfiles.remove(file)
            else:
                grism = objects.loc[objects["filename"] == objectfile][
                    "dispname"
                ].values[0]
                sensfiles.append(self.grab_sensfunc(grism))
        print(sensfiles)
        header = fits.getheader(spec1dfiles[0])
        spectrograph = load_spectrograph(header["PYP_SPEC"])

        # Parameters
        spectrograph_def_par = spectrograph.default_pypeit_par()
        par = pypeitpar.PypeItPar.from_cfg_lines(
            cfg_lines=spectrograph_def_par.to_config(), merge_with=[]
        )

        # Instantiate
        FxCalib = fluxcalibrate.FluxCalibrate.get_instance(
            spec1dfiles, sensfiles, par=par["fluxcalib"]
        )

    def grab_sensfunc(self, grism):
        try:
            path = os.path.join(self.FORSIfy_path, "data/sensfunc/", grism, "*.fits")
            return glob.glob(path)[0]
        except:
            raise IOError("Grism not included!")

    def copy_archival_masters(self, grism):
        from shutil import copytree

        path = os.path.join(
            self.FORSIfy_path, "data", "archival_calibs", grism, "Masters"
        )
        print(path)
        copytree(path, os.path.join(os.path.split(self.working_dir)[0], "Masters"))

    def create_archival_data_symlinks(self, grism):
        all_files = []
        path = os.path.join(
            self.FORSIfy_path, "data", "archival_calibs", grism, "20*", "*"
        )
        for type in ["arc", "flats", "bias"]:
            filepath = os.path.join(path, type, "*.fits")
            files_of_type = glob.glob(filepath)
            all_files += files_of_type
        for file in all_files:
            filename = os.path.split(file)[1]
            symlink_force(file, os.path.join(self.data_dir, filename))

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
        self.pypeit_header = "[rdx]\n"
        self.pypeit_header += "spectrograph = vlt_fors2\n"
        self.pypeit_header += "[calibrations]\n"
        self.pypeit_header += "[[slitedges]]\n"
        self.pypeit_header += "sync_predict = nearest\n"
        self.pypeit_header += "[reduce]\n"
        self.pypeit_header += "[[findobj]]\n"
        self.pypeit_header += "find_fwhm = 2\n"
        if self.args.sources > 0:
            self.pypeit_header += "maxnumber =" + str(self.sources) + "\n"
        self.pypeit_header += "setup read\n"
        self.pypeit_header += "Setup A:\n"
        self.pypeit_header += "setup end\n"
        self.pypeit_header += "data read\n"
        self.pypeit_header += "path " + self.data_dir + "\n"
