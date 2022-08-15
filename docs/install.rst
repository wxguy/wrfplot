==================
Installation Guide
==================

There are multiple ways you can install wrfplot. You can choose any of the methods you are comfortable in. The documentation written here are in recommanded hierarchy. Each one are listed below.

Standalone
~~~~~~~~~~

Standalone Method (Recommanded)::

	$ wget 
	$ 

Conda
~~~~~~
Conda Method::

	$ conda install -c conda-forge wrfplot


Pip
~~~~~~

Pip Method::

	$ sudo apt update && sudo apt install build-essential gfortran libhdf5-mpich-dev libpng-dev libnetcdff-dev
	$ pip install wrfplot


From Source
~~~~~~~~~~~
The wrfplot application relies on Python module ``wrf-python``. Hence you need to install these packages first.

.. warning::
  Installing ``wrf-python`` Python module under Windows OS is cumbersome process. It is highly recommended that you follow any of the above methods, if your OS is Windows.

Before proceeding to install wrfplot, ensure to install following system libraries that are required for compiling Python modules from your favourite distro. Following is the procedure required to be done for Debian/Ubuntu based distros::

	$ sudo apt update && sudo apt install build-essential gfortran libhdf5-mpich-dev libpng-dev libnetcdff-dev

Required Dependencies
=====================

Following Python modules are the basic dependencies of wrfplot:

* Python 3.5+
* numpy (1.11 or later; 1.14 required to build on Windows)
* wrapt (1.10 or later)
* setuptools (38.0 or later)
* xarray (0.7.0 or later)
* netCDF4-python (1.2.0 or later)
* matplotlib (1.4.3 or later)
* cartopy (0.13 or later)


Once everting is installed execute the below command::

	git clone https://github.com/wxguy/wrfplot
    cd wrfplot
    python setup.py install 


Confirm Installation
~~~~~~~~~~~~~~~~~~~~~

Once you install wrfplot using one of the above mentioned, you must ensure that it is installed successfully. For this you can execute following command from terminal::

	$ wrfplot --help
	usage: wrfplot.py [-h] [--list-vars] [--input <input_file>] [--output <output_dir>] [--vars <variables>]
	                  [--dpi <value>] [--list-cmaps]

	Command line application to plot static WRF model prognostic products...

	options:
	  -h, --help            show this help message and exit
	  --list-vars           List variables supported by wrfplt.
	  --input <input_file>  Mandatory path to WRF generated netCDF.
	  --output <output_dir>
	                        Path to output directory for saving images.
	  --vars <variable(s)>  Name of the variable to be plotted. Multiple variables are to be separated with ','. Use '--
	                        list-vars' option to see list of supported variables.
	  --dpi <value>         Increase or decrease the plotted image resolution. Default is 125. More is higher resolution
	                        and less is course resolution. Higher values will reduce the speed of plot .
	  --list-cmaps          List colour maps (cmaps) supported by wrfplt.

	© J Sundar, wrf.guy@gmail.com, 2022

If you get inbuilt help page of ``wrfplot``, then it is ensured that you have successfully installed wrfplot.

Uninstall
~~~~~~~~~

The uninstallation depends on the system you used to install wrfplot. Either you did it via conda (see Uninstallation via conda), via pip or from the source files (see Uninstallation via pip).

Uninstallation via conda
========================

If you installed wrfplot via conda, simply run::

	conda remove wrfplot

Uninstallation via pip
======================

Uninstalling via pip simply goes via::

	pip uninstall wrfplot
