#!/usr/bin/env python
#
# See top-level LICENSE file for Copyright information
#
# -*- coding: utf-8 -*-

import argparse
import os
from FORSify import FORSify_setup
from FORSify.util import PypeIt_to_iraf


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
    current_dir = os.getcwd()
    sort_dir = os.path.join(current_dir, "setup_files")
    FORSify = FORS_setup(sort_dir, args)
    FORSify.reduce()
    try:
        output_path = os.path.join(os.path.split(FORSify.working_dir)[0], "Output")
        os.mkdir(output_path)
    except FileExistsError:
        pass
    for key in FORSify.corresponding_files:
        new_file = key[:-5] + "_f.fits"
        converter = PypeIt_to_iraf(
            key,
            os.path.join(args.root, FORSify.corresponding_files[key]),
            output_name=str(os.path.join(output_path, os.path.split(new_file)[1])),
            linearize=True,
            overwrite=True,
            pixel=112,
            flux=True,
        )
        converter.convert()
        new_file = key[:-5] + "_c.fits"
        converter = PypeIt_to_iraf(
            key,
            os.path.join(args.root, FORSify.corresponding_files[key]),
            output_name=str(os.path.join(output_path, os.path.split(new_file)[1])),
            linearize=True,
            overwrite=True,
            pixel=112,
            flux=False,
        )
        converter.convert()
