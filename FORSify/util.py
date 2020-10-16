#!/usr/bin/env python
#
# See top-level LICENSE file for Copyright information
#
# -*- coding: utf-8 -*-

import os
import errno
import pathlib
import spectres
import numpy as np
from astropy.io import fits as pyfits


def symlink_force(target, link_name):
    try:
        os.symlink(target, link_name)
    except OSError as e:
        if e.errno == errno.EEXIST:
            os.remove(link_name)
            os.symlink(target, link_name)
        else:
            raise e


class PypeIt_to_iraf:
    def __init__(
        self,
        pypeit_file,
        observed_file,
        output_name=None,
        linearize=True,
        overwrite=True,
        pixel=112,
        flux=True,
    ):
        self.pypeit_file = pypeit_file
        self.observed_file = observed_file
        self.path_convert = pathlib.Path(__file__).parent.absolute()
        self.template_file = os.path.join(self.path_convert, "data/template.fits")
        self.linearize = linearize
        self.output_name = output_name
        self.overwrite = overwrite
        self.centered_pixel = pixel
        self.flux = flux

    def convert(self):
        self.load_pypeit()
        self.load_observed_2dspec()
        self.load_template()
        self.extract_pypeit_data()
        self.linearize_wave_grid()
        self.set_header()
        self.set_data()
        self.template.writeto(
            self.output_name, overwrite=self.overwrite, output_verify="silentfix"
        )
        print("\tOutput written to {}.".format(self.output_name))

    def load_pypeit(self):
        self.pypeit_reduction = pyfits.open(self.pypeit_file).copy()
        self.pypeit_header = self.pypeit_reduction[0].header

    def load_observed_2dspec(self):
        self.observed_2dspec = pyfits.open(self.observed_file).copy()

    def load_template(self):
        self.template = pyfits.open(self.template_file).copy()

    def get_correct_pypeit_spectrum(self):

        N_spectra = int(self.pypeit_header["NSPEC"])
        spectra_list = []
        pixel_list = []
        print("\tObjects found in pypeit reduction:")
        for i in range(N_spectra):
            exten = "EXT{:04d}".format(i)
            spectra_list.append(self.pypeit_header[exten])
            print("\t", self.pypeit_header[exten])
        for specob in spectra_list:
            pixelob = int(specob.split("-")[0][4:])
            pixel_list.append(abs(self.centered_pixel - pixelob))
        closest = spectra_list[np.argmin(pixel_list)]
        return closest

    def extract_pypeit_data(self):
        closest_object = self.get_correct_pypeit_spectrum()
        print(
            "\tClosest object to pixel #{}: ".format(self.centered_pixel),
            closest_object,
        )
        data = self.pypeit_reduction[closest_object].data
        self.pypeit_wave = data["OPT_WAVE"]
        if self.flux == True:
            keys = ["OPT_FLAM", "OPT_FLAM_SIG", "BOX_FLAM", "OPT_COUNTS_SIG"]
        else:
            keys = ["OPT_COUNTS", "BOX_COUNTS", "OPT_COUNTS_SKY", "OPT_COUNTS_SIG"]
        for key in keys:
            print(key)
        self.number_columns = len(keys)
        self.extracted_data = np.array([data[key] for key in keys])
        self.extracted_data = self.extracted_data.reshape(
            self.number_columns, 1, self.pypeit_wave.shape[0]
        )
        if self.flux == True:
            clean_extracted = []
            print(self.extracted_data.shape)
            mask = ~np.isnan(self.extracted_data[0, :, :])
            # print(mask.shape)
            self.pypeit_wave = data["OPT_WAVE"][mask.flatten()]
            clean_extracted.append(
                self.extracted_data[0, :, :][~np.isnan(self.extracted_data[0, :, :])]
                * 1e-17
            )
            clean_extracted.append(
                self.extracted_data[1, :, :][~np.isnan(self.extracted_data[0, :, :])]
                * 1e-17
            )
            clean_extracted.append(
                self.extracted_data[2, :, :][~np.isnan(self.extracted_data[0, :, :])]
            )
            clean_extracted.append(
                self.extracted_data[3, :, :][~np.isnan(self.extracted_data[0, :, :])]
            )

            self.extracted_data = np.array(clean_extracted)
            self.extracted_data = self.extracted_data.reshape(
                self.number_columns, 1, self.pypeit_wave.shape[0]
            )
            import matplotlib.pylab as plt

            plt.plot(self.pypeit_wave, self.extracted_data[1, 0, :])
            plt.show()

    def linearize_wave_grid(self):
        print(
            "\tLinearizing wavelength grid between {:.2f} A and {:.2f} A.".format(
                self.pypeit_wave[0] + 5, self.pypeit_wave[-5] - 5
            )
        )
        self.linear_wave_grid = np.linspace(
            self.pypeit_wave[0] + 5,
            self.pypeit_wave[-1] - 5,
            self.pypeit_wave.shape[0],
        )
        self.linear_extracted_data = np.array(
            [
                self.interpolate_linear(self.extracted_data[i].flatten())
                for i in range(self.number_columns)
            ]
        ).reshape(self.number_columns, 1, self.linear_wave_grid.shape[0])

    def set_data(self):
        if self.linearize == True:
            self.template[0].data = self.linear_extracted_data
        elif self.linearize == False:
            self.template[0].data = self.extracted_data

        else:
            raise ValueError("Linearize can be either True or False")
        # print(self.template[0].data[0, :, :][~np.isnan(self.template[0].data[0, :, :])])

    def interpolate_linear(self, quantity):
        return spectres.spectres(self.linear_wave_grid, self.pypeit_wave, quantity)

    def set_header(self):
        print("\tUpdating fits header.")
        self.template[0].header = self.observed_2dspec[0].header
        self.template[0].header["CTYPE1"] = "LINEAR  "
        self.template[0].header["CTYPE2"] = "LINEAR  "
        self.template[0].header["CRPIX1"] = 1.0
        self.template[0].header["EXTEND"] = "F"
        self.template[0].header.pop("CRVAL2")
        self.template[0].header.pop("CRPIX2")
        self.template[0].header.pop("BSCALE")
        self.template[0].header.pop("BZERO")
        # self.template[0].header["CD3_3"] = 1
        self.template[0].header["CRVAL1"] = np.min(self.linear_wave_grid)
        self.template[0].header["CD1_1"] = (
            self.linear_wave_grid[1] - self.linear_wave_grid[0]
        )
        self.template[0].header["CD2_1"] = 0
        self.template[0].header["CD1_2"] = 0
        pypeit_header_keywords = [
            "VERSPYT",
            "VERSNPY",
            "VERSSCI",
            "VERSAST",
            "VERSSKL",
            "VERSPYP",
            "DMODCLS",
            "DMODVER",
        ]
        for keyword in pypeit_header_keywords:
            self.template[0].header[keyword] = (
                self.pypeit_header[keyword],
                self.pypeit_header.comments[keyword],
            )
        self.template[0].header["REDDATE"] = (
            self.pypeit_header["DATE"],
            "reduction date",
        )
