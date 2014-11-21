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

REQUIRED_TAGS = ['StudyID', 'SeriesNumber', 'InstanceNumber']


def filter(filename):
    dcm = None

    try:
        dcm = dicom.read_file(filename)
    except:
        logging.debug("{0}: Not a readable DICOM".format(filename))
        return None

    if not all([hasattr(dcm, tag) for tag in REQUIRED_TAGS]):
        logging.debug("{0}: Missing required tag".format(filename))
        return None

    return dcm
