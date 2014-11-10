#!/usr/bin/env python
# Part ofthe ge-mri-rtafni package; see LICENSE for details
# Copyright (c) 2014 Board of Regents of the University of Wisconsin System

"""Realtime DICOM copier.

Usage:
  realtime_dicom_copy.py <watch_dir> <dest_dir> [options]

Options:
  -h --help               Show this screen
  --version               Show version information
  --verbose               Dump lots of logging information
  --filter-module=<mod>   [default: is_dicom] This must be the name of a
                          python module that implements a filter() method.
                          This method will take a filename and return a
                          dicom dataset or None.
"""

import os
import sys

# Add vendor directory to module search path
parent_dir = os.path.abspath(os.path.dirname(__file__))
vendor_dir = os.path.join(parent_dir, 'vendor')

sys.path.insert(1, vendor_dir)
from docopt import docopt


if __name__ == '__main__':
    arguments = docopt(__doc__, version="0.1.0")
    print(arguments)
