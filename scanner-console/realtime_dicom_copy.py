#!/usr/bin/env python
# Part ofthe ge-mri-rtafni package; see LICENSE for details
# Copyright (c) 2014 Board of Regents of the University of Wisconsin System

"""Realtime DICOM copier.

Usage:
  realtime_dicom_copy.py <watch_dir> <dest_dir> [options]

Options:
  -h --help               Show this screen
  --version               Show version information
  -v --verbose            Show lots of logging information
  --filter-module=<mod>   [default: is_dicom] This must be the name of a
                          python module that implements a filter() method.
                          This method will take a filename and return a
                          dicom dataset or None.
"""

import os
import sys
import shutil
import logging

# Add vendor directory to module search path
parent_dir = os.path.abspath(os.path.dirname(__file__))
vendor_dir = os.path.join(parent_dir, 'vendor')

sys.path.insert(1, vendor_dir)
from docopt import docopt
import pyinotify


class DicomCopier(pyinotify.ProcessEvent):

    def my_init(self, dicom_filter, dest_base):
        self.dicom_filter = dicom_filter
        self.dest_base = dest_base

    def process_default(self, event):
        """ Handle a file creation/move event.

        This determines whether it's an appropriate DICOM with the filter,
        then gets (or creates) a directory for it, and copies the file.
        """
        dcm = self.dicom_filter.filter(event.pathname)
        if dcm:
            dest_dir = self._make_or_get_dest_dir(dcm)
            if dest_dir:
                shutil.copy(event.pathname, dest_dir)
                logging.debug("{0} -> {1}/{2}".format(
                    event.pathname,
                    dest_dir,
                    os.path.basename(event.pathname)))
        else:
            logging.debug("{0} is not a dicom.".format(event.pathname))

    def _make_or_get_dest_dir(self, dcm):
        """ Computes a directory name for a dicom, and creates it if needed.

        Returns either a pathname or None if we can't figure one out.
        """

        dirname = "e{0}-s{1}".format(
            dcm.get("StudyID"), dcm.get("SeriesNumber"))
        dest_dir = os.path.join(self.dest_base, dirname)
        if not os.path.isdir(dest_dir):
            logging.info("Creating directory: {0}".format(dest_dir))
            os.makedirs(dest_dir)
        return dest_dir


def watch_for_dicoms(watch_dir, dest_dir, dicom_filter):
    wm = pyinotify.WatchManager()
    handler = DicomCopier(
        dicom_filter=dicom_filter,
        dest_base=dest_dir)
    notifier = pyinotify.Notifier(wm, default_proc_fun=handler)
    watch_mask = (
        pyinotify.IN_MOVED_TO |
        pyinotify.IN_CLOSE_WRITE |
        pyinotify.IN_CREATE)
    wm.add_watch(watch_dir, watch_mask, rec=True, auto_add=True)
    logging.info("Watching {0} for dicoms".format(watch_dir))
    notifier.loop()


def main(arguments):
    log_level = logging.INFO
    if arguments.get("--verbose"):
        log_level = logging.DEBUG
    logging.basicConfig(
        format="%(message)s", stream=sys.stderr, level=log_level)
    logging.debug("Starting with arguments:")
    logging.debug(arguments)
    dicom_filter = __import__(arguments.get("--filter-module"))
    watch_for_dicoms(
        arguments['<watch_dir>'],
        arguments['<dest_dir>'],
        dicom_filter)


if __name__ == '__main__':
    arguments = docopt(__doc__, version="0.1.0")
    main(arguments)
