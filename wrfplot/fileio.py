#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Do input output operation for a given input file """
"""
This file is part of wrfplot application.

wrfplot is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as
 published by the Free Software Foundation, either version 3 of the License, or any later version. 
 
wrfplot is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty 
of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with wrfplot. If not, 
see <http://www.gnu.org/licenses/>.
"""

__author__ = "J Sundar (wrf.guy@gmail.com)"

import os
import netCDF4 as nc


class FileIO(object):
    """Do IO operation on input file"""

    def __init__(self, filepath):
        super(FileIO, self).__init__()
        self.filepath = filepath
        self.file_type = None
        self.header = self.read_file()

    def validate_file(self):
        if not os.path.exists(self.filepath):
            raise ("")

    def read_file(self):
        """Read only header leangth of 120 bytes"""
        with open(self.filepath, errors="ignore") as f:
            self.header = f.read(120)

    def is_grib2(self):
        """Check if given file is GRIB type"""
        if "GRIB" in self.header:
            self.file_type = "grib2"
            return True

    def is_netcdf(self):
        """Check if given file is NetCDF type"""
        if "CDF" in self.header:
            self.file_type = "netcdf"
            return True

    def is_wrf(self):
        """Check if given file is WRF model output"""
        if self.is_netcdf:
            _file = nc.Dataset(self.filepath, "r")
            if "MP_PHYSICS" in _file.ncattrs():
                return True
            else:
                False
