# ge-mri-afni

#### Tools to enable realtime fMRI data monitoring on GE scanners

If you came to town looking for a special-purpose software package, you sure have come to the right place. This is a little package to enable monitoring fMRI data collection from GE's MRI scanners, using AFNI's Dimon and viewer. It might work with other kinds of scanners, too; it'll really depend on whether Dimon likes your dicoms.

This was developed at and for the Waisman Laboratory for Brain Imaging at the University of Wisconsin–Madison. It might be useful other places, too. But I'm not very likely to help you make it work.

There are two main components to this:

### Scanner console uploader

This is designed to have the minimal possible footprint on the running scanner. It uses inotify (really, pyinotify) to watch for incoming files in the dicom store and copy them to an NFS-mounted directory on the data upload host.

It does use pydicom to decide what files to copy (let's not bother with things that aren't dicoms) and where to put them (<exam>-<series>). We don't rely on the handler on the upload host to sort the files, as we don't know the handler will be running when we start copying files.

Really, though: just leave the damn handler running.

### Data upload host

This does some More Stuff.

The basic idea here is that we watch an incoming directory (and all subdirs) for new files. When we get one:

* Is it a dicom? If not, continue. Else:
** Stop watching the directory this file came into.
** Figure out some scan parameters. If we want to realtime this scan (what's that criteria?) run a script that starts Dimon with the appropriate flags.
** At the end of that script, delete the scan's directory.

### Dependencies and credits

Requires python 2.6. Probably won't work with 3.x.

This package tries to be free of external dependencies; therefore, we ship with several excellent libraries:

* [pydicom](https://code.google.com/p/pydicom/) Copyright (c) 2008-2010 Darcy Mason and pydicom contributors
* [pyinotify](https://github.com/seb-m/pyinotify) Copyright (c) 2010 Sebastien Martini <seb@dbzteam.org>
* [docopt](https://github.com/docopt/docopt) Copyright (c) 2012 Vladimir Keleshev, <vladimir@keleshev.com>

ge-mri-rtafni was written by Nate Vack <njvack@wisc.edu> and is Copyright 2014 the Board of Regents of the University of Wisconsin System. It's MIT-licensed; see LICENSE if you don't know what that means.