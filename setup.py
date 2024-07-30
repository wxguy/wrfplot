#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Standard setup.py file for wrfplot """
"""
This file is part of wrfplot application.

wrfplot is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as
 published by the Free Software Foundation, either version 3 of the License, or any later version. 
 
wrfplot is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty 
of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with wrfplot. If not, 
see <http://www.gnu.org/licenses/>.
"""

__author__ = 'J Sundar (wrf.guy@gmail.com)'

import io
import os
import glob
from setuptools import find_packages, setup

# Package meta-data.
NAME = 'wrfplot'
DESCRIPTION = 'Command line application to plot WRF model output data...'
URL = 'https://github.com/wxguy/wrfplot'
EMAIL = 'wrf.guy@gmail.com'
AUTHOR = 'J Sundar'
REQUIRES_PYTHON = '>=3.7.0'
VERSION = None
LICENSE = 'GNU General Public License v3 (GPLv3)'

# What packages are required for this module to be executed?
REQUIRED = ['cartopy', 'xarray', 'matplotlib', 'wrf-python>=1.3', 'tqdm', 'netcdf4']

here = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = '\n' + f.read()

about = {}
if not VERSION:
    with open(os.path.join(here, NAME, '_version.py')) as f:
        exec(f.read(), about)
else:
    about['__version__'] = VERSION


def list_files(directory):
    files = []
    all_files = glob.glob(directory + '/**/*', recursive=True)
    for _file in all_files:
        if os.path.isfile(_file) and '.py' not in _file:
            files.append(_file)
    return files


def _version():
    from setuptools_scm.version import SEMVER_MINOR, guess_next_simple_semver, release_branch_semver_version, simplified_semver_version

    def my_release_branch_semver_version(version):
        v = release_branch_semver_version(version)
        if v == version.format_next_version(guess_next_simple_semver, retain=SEMVER_MINOR):
            return version.format_next_version(guess_next_simple_semver, fmt="{guessed}", retain=SEMVER_MINOR)
        return v

    return {
        'version_scheme': my_release_branch_semver_version,
        'local_scheme': 'no-local-version',
    }


setup(
    name=NAME,
    use_scm_version=True, # _version
    setup_requires=['setuptools_scm'],
    description=DESCRIPTION,
    long_description=long_description,
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    keywords=["Scientific", "Engineering", "Atmospheric Science", "Weather Model", "Plotting", "Software Development",
              "Numerical Weather Prediction", "NWP", "Weather Research and Forecast", "WRF"],
    py_modules=['wrfplot'],

    entry_points={
        'console_scripts': ['wrfplot=wrfplot.wrfplot:main'],
    },
    install_requires=REQUIRED,
    license=LICENSE,
    classifiers=[
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: Unix',
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Scientific/Engineering :: Atmospheric Science',
        'Topic :: Scientific/Engineering :: Numerical Weather Model',
        'Topic :: Scientific/Engineering :: WRF',
        'Topic :: Scientific/Engineering :: Visualization',
    ],
    packages=find_packages("wrfplot", exclude=['test', 'test.*'],),
    include_package_data=True,
    exclude_package_data={'': ['test']},
    package_dir={'wrfplot': 'wrfplot'},
    package_data={'wrfplot': ['colormaps/colormaps/cartocolors/*',
                              'colormaps/colormaps/cmocean/*',
                              'colormaps/colormaps/colorbrewer/*',
                              'colormaps/colormaps/colorcet/*',
                              'colormaps/colormaps/cubehelix/*',
                              'colormaps/colormaps/ncar_ncl/*',
                              'colormaps/colormaps/scientific/*',
                              'colormaps/colormaps/sciviz/*',
                              'colormaps/colormaps/tableau/*',
                              'data/*', 'data/shapefiles/natural_earth/cultural/*',
                              'data/shapefiles/natural_earth/physical/*', 'data/shape/*']},
    # package_data={'wrfplot': list_files('wrfplot')},
    # $ setup.py publish support.
    # cmdclass={ 'upload': UploadCommand,},
    project_urls={
        "Bug Reports": "https://github.com/wxguy/wrfplot/issues",
        "Source": "https://github.com/wxguy/wrfplot",
        "Documentation": "https://wxguy.in/wrfplot"
    },
)
