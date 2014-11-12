# Part ofthe ge-mri-rtafni package; see LICENSE for details
# Copyright (c) 2014 Board of Regents of the University of Wisconsin System


"""
This filter determines whether a dicom is an fmri dicom, based on pulse
sequence name. For GE dicoms, this is a filename stored in the private tag
(0x0019, 0x109c). We're looking for the filename to be 'fmri'.

We also require 'StudyID' and 'SeriesNumber' though those really should exist
for any fmri dicom.
"""

import os
import logging
import dicom

PULSE_SEQUENCE_TAG = (0x0019, 0x109c)
FMRI_NAMES = set(['fmri', 'epirt', 'epirt_20', 'epirt_22'])


def filter(filename):
    dcm = None
    try:
        dcm = dicom.read_file(filename)
    except:
        logging.debug("{0}: Not a readable DICOM".format(filename))
        return None

    identifiable = hasattr(dcm, 'StudyID') and hasattr(dcm, 'SeriesNumber')
    psd_name = ""
    try:
        psd_name = str(dcm[PULSE_SEQUENCE_TAG].value)
    except:
        logging.debug("{0}: Can't determine pulse sequence name".format(
            filename))
        return None
    psd_name = os.path.basename(psd_name).lower()
    if identifiable and psd_name in FMRI_NAMES:
        return dcm
    return None
