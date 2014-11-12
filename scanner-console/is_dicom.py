# Part ofthe ge-mri-rtafni package; see LICENSE for details
# Copyright (c) 2014 Board of Regents of the University of Wisconsin System

"""
This is the bare-bones filter that returns a dicom if a pathname is one and
can be used by the copier (eg, has StudyID and SeriesNumber)

Filter modules must implement a function called filter() that takes a
filename. This function will either return a Dicom (from pydicom) or None.
"""

import logging
import dicom


def filter(filename):
    dcm = None
    try:
        dcm = dicom.read_file(filename)
    except:
        logging.debug("{0}: Not a readable DICOM".format(filename))
    if hasattr(dcm, 'StudyID') and hasattr(dcm, 'SeriesNumber'):
        return dcm
    return None
