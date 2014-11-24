# ge-mri-afni

#### Tools to enable realtime fMRI data monitoring on GE scanners

If you came to town looking for a special-purpose software package, you sure have come to the right place. This is a little package to enable monitoring fMRI data collection from GE's MRI scanners, using AFNI's Dimon and viewer. It might work with other kinds of scanners, too; it'll really depend on whether Dimon likes your dicoms.

This was developed at and for the Waisman Laboratory for Brain Imaging at the University of Wisconsin–Madison. It might be useful other places, too. But I'm not very likely to help you make it work.

There are two main components to this:

### Scanner console uploader

This is designed to have a minimal footprint on the running scanner. It uses inotify (really, pyinotify) to watch for incoming files in the dicom store and copy them to an NFS-mounted directory on the data upload host.

The program you'll run on the scanner console is `realtime_dicom_copy`:

```
Realtime DICOM copier.

Usage:
  realtime_dicom_copy.py <watch_dir> <dest_dir> [options]

Options:
  -h --help               Show this screen
  --version               Show version information
  -v --verbose            Show lots of logging information
  --filter-module=<mod>   [default: is_dicom] This must be the name of a
                          python module that implements a filter() method.
                          This method will take a filename and return a
                          dicom dataset or None/False.
```

See `is_dicom.py` and `fmri_dicom.py` in the `scanner-console` directory to see how the filters work.

For us, the command `realtime_dicom_copy.py /export/home1/sdc_image_pool/images /mri-upload/rtafni --filter=fmri_dicom` starts things working nicely.


### Data upload host

This does some More Stuff.

The basic idea here is that we watch an incoming directory (and all subdirs) for new files. When we get one:

* Is it a dicom? If not, continue. Else:
* Stop watching the directory this file came into.
* From the dicom, determine the number of frames and slices per frame
* Kick off the viewer script (see `upload-host/bash/rtafni.sh`)

The script you're using here is `upload-host/realtime_monitor.py`:

```
Watch for DICOM series and start a realtime viewer. Probably realtime AFNI.

Usage:
  realtime_monitor.py <watch_path> <realtime_script> [options]

Options:
  -h --help
  -v --verbose

realtime_script will be called with three arguments:
  The path to the DICOM series
  The number of expected slices per frame
  The number expected frames
```

`upload-host/bash/rtafni.sh` is a pretty good stab at a `realtime_script`.

Remember that because of the Magic of X11, your upload host need not be the computer you're viewing the data on.

### Dependencies and credits

Requires python 2.6. Probably won't work with 3.x.

This package tries to be free of external dependencies; therefore, we ship with several excellent libraries:

* [pydicom](https://code.google.com/p/pydicom/) Copyright (c) 2008-2010 Darcy Mason and pydicom contributors
* [pyinotify](https://github.com/seb-m/pyinotify) Copyright (c) 2010 Sebastien Martini <seb@dbzteam.org>
* [docopt](https://github.com/docopt/docopt) Copyright (c) 2012 Vladimir Keleshev, <vladimir@keleshev.com>

ge-mri-rtafni was written by Nate Vack <njvack@wisc.edu> and is Copyright 2014 the Board of Regents of the University of Wisconsin System. It's MIT-licensed; see LICENSE if you don't know what that means.