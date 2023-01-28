[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

[![Linux](https://svgshare.com/i/Zhy.svg)](https://svgshare.com/i/Zhy.svg) [![Windows](https://svgshare.com/i/ZhY.svg)](https://svgshare.com/i/ZhY.svg)

[![Documentation Status](https://readthedocs.org/projects/wrfplot/badge/?version=latest)](https://wrfplot.readthedocs.io/en/latest/?badge=latest)

[![PyPI Version](https://badge.fury.io/py/ansicolortags.svg)](https://pypi.python.org/pypi/wrfplot/) [![PyPi Downloads](https://static.pepy.tech/personalized-badge/wrfplot?period=total&units=international_system&left_color=blue&right_color=brightgreen&left_text=Pip%20Downloads)](https://pepy.tech/project/wrfplot)

![Build and Release](https://github.com/wxguy/wrfplot/actions/workflows/release-github.yaml/badge.svg)  ![PyPi Package](https://github.com/wxguy/wrfplot/actions/workflows/release-pip.yaml/badge.svg)

## About wrfplot

**wrfplot** is a command line application written in Python programming language to plot set of diagnostic variables from World Research and Forecasting (WRF) atmospheric model output file. Though, WRF model output files are simple NetCDF, it requires one to install various software and libraries to plot a few variables.  Python has many modules that can deal with WRF model output data set. However, setting up theses libraries, plotting variables through reading lot of documentation is tedious process. **wrfplot** aims to fill this gap by proving an application that is easy to install and use. 

The idea of developing wrfplot came to my mind as I frequently revisit the same code base again and again to tweak few lines of code to get changes in final plots. Therefore, I was looking for a command line application that would help me to tweak the common WRF model forecast images by providing appropriate command line options. I could not find any and hence created one.

## Documentation

Documentation of this project is located at https://wrfplot.readthedocs.io.

## Use Cases

A typical use case of wrfplot would be to include as part of your WRF model run framework to plotting of variables immediately after the model run is completed. The other use case would be to use it for producing publication quality 2D maps which does not much tweaking for your publication.

## Installation

Since it is intended to be used as command line, the application is distributed as stand-alone on both Linux and Windows. You must download the correct version of application installer or setup file. Both are described below:

### Windows

Go to https://github.com/wxguy/wrfplot/releases and look for latest release. The Windows setup executable will have name `wrfplot-windows-64bit.exe`. Click on the link and download it to local disk. The rest of the installation procedure is same as you do for any other windows setup files. Once installed Check if installation is successful by typing following command in `cmd` window which should not produce any errors:

```
wrfplot --version
0.1.0
```

### Linux

 Go to https://github.com/wxguy/wrfplot/releases and look for latest release. The Linux installer will have name `wrfplot-linux-64bit.run`. Click on the link and download it to local disk. Thereafter execute the below command (assuming that the Linux installer is downloaded at `~/Downloads`):

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

Once installed Check if installation is successful by typing following command in terminal which should not produce any errors:

```
wrfplot --version
0.1.0
```

## How to use?

Please refer to https://wrfplot.readthedocs.io for complete documentation on how to use `wrfplot` application.


## TODO

Add following command line options:

* `--levels `   :   To plot upper level data as per user defined levels
* `--cmap`      :   Use user provided colour map
* `--contours`  :   Control contour levels
* `--animation` :   Create animation for specific variable(s) in GIF for max compatibility
* `--fig-format`:   Save image in specific file format
* `--list-fig-format`   :   List all supported image file format
* `--title`     :   Custom title for the plot
* `--title-font-size`   :   Specify title font size

## Author

J Sundar aka WxGuy (wrf.guy@gmail.com)
