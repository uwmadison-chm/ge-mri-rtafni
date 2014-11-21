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
REQUIRED_TAGS = ['StudyID', 'SeriesNumber', 'InstanceNumber']


def filter(filename):
    dcm = None
    try:
        dcm = dicom.read_file(filename)
    except:
        logging.debug("{0}: Not a readable DICOM".format(filename))
        return None

    identifiable = all([hasattr(dcm, tag) for tag in REQUIRED_TAGS])
    if not identifiable:
        logging.debug("{0}: Missing required tag".format(filename))
        return None

    psd_name = ""
    try:
        psd_name = str(dcm[PULSE_SEQUENCE_TAG].value)
    except:
        logging.debug("{0}: Can't determine pulse sequence name".format(
            filename))
        return None
    psd_name = os.path.basename(psd_name).lower()
    if psd_name not in FMRI_NAMES:
        logging.debug("{0}: {1} not for fMRI".format(
            filename, psd_name))
        return None
    return dcm
