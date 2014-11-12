# Part ofthe ge-mri-rtafni package; see LICENSE for details
# Copyright (c) 2014 Board of Regents of the University of Wisconsin System

import dicom

"""
This is the bare-bones filter that returns a dicom if a pathname is one and
can be used by the copier (eg, has StudyID and SeriesNumber)

Filter modules must implement a function called filter() that takes a
filename. This function will either return a Dicom (from pydicom) or None.
"""


def filter(filename):
    dcm = None
    try:
        dcm = dicom.read_file(filename)
    except:
        pass
    if hasattr(dcm, 'StudyID') and hasattr(dcm, 'SeriesNumber'):
        return dcm
    return None
