#!/usr/bin/env python

"""Watch for DICOM series and start a realtime viewer. Probably realtime AFNI.

Usage:
  realtime_monitor.py <watch_path> <realtime_script> [options]

Options:
  -h --help
  -v --verbose

realtime_script will be called with three arguments:
  The path to the DICOM series
  The number of expected slices per frame
  The number expected frames

"""


import os
import sys
import subprocess
import logging

# Add vendor directory to module search path
parent_dir = os.path.abspath(os.path.dirname(__file__))
vendor_dir = os.path.join(parent_dir, 'vendor')

sys.path.insert(1, vendor_dir)
from docopt import docopt
import pyinotify
import dicom
pyinotify.log.setLevel(logging.ERROR)


class DicomWatcher(pyinotify.ProcessEvent):
    """
    This watcher will see a DICOM, look for its total expected frames and
    slices, and then spawn a viewer on the parent directory.

    Equally important: it will *stop* watching the parent directory, so we
    only run *one* viewer.

    Another way to do this would be to create a .realtime file in the parent
    directory and then check for that before launching, but this seems
    cleaner and less events-y. We shall see.
    """
    def my_init(self, realtime_script, watch_manager):
        self.realtime_script = realtime_script
        self.watch_manager = watch_manager

    def process_IN_CLOSE_WRITE(self, event):
        # Check for dicomness. If it's a dicom, unwatch this directory and
        # start the viewer.
        dcm = None
        frames = 0
        slices = 0
        try:
            dcm = dicom.read_file(event.pathname)
            frames = str(dcm.NumberOfTemporalPositions)
            slices = str(dcm.ImagesInAcquisition)
        except:
            logging.info("{0}: Not a readable dicom".format(event.pathname))
            return
        # Remove watch on parent dir
        self.watch_manager.rm_watch(event.wd)
        parent_dir = os.path.dirname(event.pathname)
        logging.info("Opening viewer for {0}".format(parent_dir))
        subprocess.Popen(
            [self.realtime_script, parent_dir, slices, frames],
            close_fds=True)


def watch_for_dicoms(watch_path, realtime_script):
    wm = pyinotify.WatchManager()
    handler = DicomWatcher(
        realtime_script=realtime_script,
        watch_manager=wm)
    notifier = pyinotify.Notifier(wm, default_proc_fun=handler)
    watch_mask = (pyinotify.IN_CREATE | pyinotify.IN_CLOSE_WRITE)
    wm.add_watch(watch_path, watch_mask, rec=True, auto_add=True)
    logging.info("Watching {0} for dicoms".format(watch_path))
    notifier.loop()


def main():
    arguments = docopt(__doc__, version="0.1")
    log_level = logging.INFO
    if arguments.get("--verbose"):
        log_level = logging.DEBUG
    logging.basicConfig(
        format="%(message)s", stream=sys.stderr, level=log_level)
    logging.debug("Starting with arguments:")
    logging.debug(arguments)
    print(arguments)
    watch_for_dicoms(
        arguments['<watch_path>'],
        arguments['<realtime_script>'])


if __name__ == '__main__':
    main()
