#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "J Sundar (wrf.guy@gmail.com)"

"""Make python treat directory as package

The __init__.py is a special file in Python. Presence of this file in a directory containing other python script will
 be interpreted as a package. Normally nothing to be written on this file. However, to make wrfplot work in
development and post install mode the single line is to added in to path.

(C) J Sundar, 2024

Released under GNU Public License (GPL) Version 3 or above. Therefore, you are free to copy, use, edit any part of the
 code from this file or any other file from the wrfplot program. However, you may not remove the original author's
name or any other information related to author such as email id, contact number etc. You may also give credit to 
original author wherever wrfplot is used or referred.

"""

from importlib.metadata import version

import sys
import os

# Ensure that package directory is added in to system path so that it works on
# development and post install mode
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

name = "wrfplot"

try:
    __version__ = version("wrfplot")
except:
    # package is not installed
    # Get the version from local file
    import _version
    __version__ = _version.__version__
finally:
    # Do nothing
    pass

