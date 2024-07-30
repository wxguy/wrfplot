Application License [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

Works on both Linux [![Linux](https://skillicons.dev/icons?i=linux)](https://github.com/wxguy/wrfplot/releases) and Windows [![Windows](https://skillicons.dev/icons?i=windows)](https://github.com/wxguy/wrfplot/releases). 

Mac OS [![macOS](https://skillicons.dev/icons?i=apple)](https://anaconda.org/search?q=wrfplot) support is available via `conda`.

Status of Documentation [![Documentation    ](https://github.com/wxguy/wrfplot/actions/workflows/build-docs.yaml/badge.svg)](https://github.com/wxguy/wrfplot/actions/workflows/build-docs.yaml/badge.svg)

Details of PyPi package [![PyPI Version](https://badge.fury.io/py/ansicolortags.svg)](https://pypi.python.org/pypi/wrfplot/) [![PyPi Downloads](https://static.pepy.tech/personalized-badge/wrfplot?period=total&units=international_system&left_color=blue&right_color=brightgreen&left_text=Pip%20Downloads)](https://pepy.tech/project/wrfplot)

Status of builds ![Build and Release](https://github.com/wxguy/wrfplot/actions/workflows/release-github.yaml/badge.svg)  ![PyPi Package](https://github.com/wxguy/wrfplot/actions/workflows/release-pip.yaml/badge.svg)

Conda details ![Conda Version](https://img.shields.io/conda/v/conda-forge/wrfplot)  ![Last updated on](https://anaconda.org/conda-forge/wrfplot/badges/latest_release_date.svg) ![Works on Windows, Linux and Mac](https://anaconda.org/conda-forge/wrfplot/badges/platforms.svg) ![Download Counts](https://img.shields.io/conda/dn/conda-forge/wrfplot)

## About wrfplot

**wrfplot** is a command line application written in Python programming language to plot set of diagnostic variables from World Research and Forecasting (WRF) atmospheric model output file. Though, WRF model output files are simple NetCDF, it requires one to install various software and libraries to plot a few variables.  Python has many modules that can deal with WRF model output data set. However, setting up theses libraries, plotting variables through reading lot of documentation is tedious process. **wrfplot** aims to fill this gap by proving an application that is easy to install and use. 

The idea of developing wrfplot came to my mind as I frequently revisit the same code base again and again to tweak few lines of code to get changes in final plots. Therefore, I was looking for a command line application that would help me to tweak the common WRF model forecast images by providing appropriate command line options. I could not find any and hence created one.

## Documentation

Documentation of this project is located at https://wxguy.in/wrfplot.

## Use Cases

A typical use case of wrfplot would be to include as part of your WRF model run framework to plotting of variables immediately after the model run is completed. The other use case would be to use it for producing publication quality 2D maps which does not much tweaking for your publication.

## Installation on all Platforms (Windows, Linux and Mac OS)

Support for all platforms is provided through `conda-forge`. If you have already conda installed, then following command is enough to install `wrfplot`:

```
conda install -c cond-forge wrfplot
```
Check your installation by typing the following command which should show the version number:

```
wrfplot --version
0.1.0
```


## Binary (standalone) Installation

Since it is intended to be used as a command line, the application is also distributed as stand-alone on both Linux and Windows. You must download the correct version of application installer or setup file. Both are described below:

### Windows Only

Go to https://github.com/wxguy/wrfplot/releases and look for the latest release. The Windows setup executable will have name `wrfplot-windows-64bit.exe`. Click on the link and download it to local disk. The rest of the installation procedure is same as you do for any other windows setup files. Once installed Check if installation is successful by typing following command in `cmd` window which should not produce any errors:

```
wrfplot --version
0.1.0
```

### Linux Only

 You must have at least `Ubuntu 22.04` , `Red Hat 8.x` or above for this to work. There is no additional packages or admin rights are required to install this package. Go to https://github.com/wxguy/wrfplot/releases and look for latest release. The Linux installer will have name `wrfplot-linux-64bit.run`. Click on the link and download it to local disk. Thereafter execute the below command (assuming that the Linux installer is downloaded at `~/Downloads`):

 ```
 bash ~/Downloads/wrfplot-linux-64bit.run
 ```

 that would produce the output as indicated below:

 ```
Verifying archive integrity...  100%   MD5 checksums are OK. All good.
Uncompressing wrfplot_Linux_Installer  100%  
Removing previous install directory...
Installing wrfplot to /home/wxguy/.wrfplot...
Renaming '/home/wxguy/wrfplot' directory to '/home/wxguy/.wrfplot'..
'/home/wxguy/.local/bin' directory already exists. Not creating it.
Linking wrfplot executable...
Updating .bashrc file to include install directory...
/home/wxguy/.local/bin directory already added to PATH. Skipping...
Installation completed. Please restart your terminal to continue using wrfplot...
```

Once installed Check if installation is successful by typing the following command in the terminal which should not produce any errors:

```
wrfplot --version
0.1.0
```

### macOS Only

At the moment, macOS support is not available in binary format. However, support is provided through conda. You can install `wrfplot` using `conda install -c cond-forge wrfplot` command.

## How to use?

Please refer to https://wxguy.in/wrfplot for complete documentation on how to use `wrfplot` application.


## TODO

Add the following command line options:

* ~~`--cmap`      :   Use user provided colour map~~
* ~~`--ulevels `   :   To plot upper level data as per user defined upper levels~~
* `--clevels `   :   Control contour levels
* ~~`--animation` :   Create animation for specific variable(s) in GIF for max compatibility~~. The animation option is implemented through `--gif` and `--gif-speed` options. Completed.
* `--save-format`:   Save image in specific file format
* `--list-save-format`   :   List all supported image file format
* `--title`     :   Custom title for the plot
* `--title-font-size`   :   Specify title font size

## Author

J Sundar (wrf.guy@gmail.com)
