==================
Installation Guide
==================

Since it is intended to be used as command line, the application is distributed as stand-alone on both Linux and Windows. You must download the correct version of application installer or setup file. Both are described below:

Windows
~~~~~~~

Go to https://github.com/wxguy/wrfplot/releases and look for latest release. The Windows setup executable will have name `wrfplot-windows-64bit.exe`. Click on the link and download it to local disk. The rest of the installation procedure is same as you do for any other windows setup files. Here are the complete process of installing in visual format:

.. image:: _static/images/screenshots/1-windows-setup.png
  :width: 500
  :alt: Windows Setup File

.. image:: _static/images/screenshots/2-user-elivation.png
  :width: 400
  :alt: Windows User Elevation

.. image:: _static/images/screenshots/3-windows-welcome-screen.png
  :width: 400
  :alt: Windows Welcome Screen

.. image:: _static/images/screenshots/4-windows-user-agreement.png
  :width: 400
  :alt: Windows User Agreement

.. image:: _static/images/screenshots/5-windows-install-options.png
  :width: 400
  :alt: Windows Install Options

.. image:: _static/images/screenshots/6-windows-destination-dir.png
  :width: 400
  :alt: Windows Install Directory

.. image:: _static/images/screenshots/7-windows-install-progress.png
  :width: 400
  :alt: Windows Install Progress

.. image:: _static/images/screenshots/8-windows-install-finish.png
  :width: 400
  :alt: Windows Finish Screen


Linux
~~~~~~

 Go to https://github.com/wxguy/wrfplot/releases and look for latest release. The Windows setup executable will have name `wrfplot-linux-64bit.run`. Click on the link and download it to local disk. Thereafter execute the below command (assuming that the Linux installer is downloaded at `~/Downloads`)::

 	$ bash ~/Downloads/wrfplot-linux-64bit.run
 

 that would produce the output as indicated below::


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


Confirm Installation
~~~~~~~~~~~~~~~~~~~~~

Once you install wrfplot using one of the above mentioned, you must ensure that it is installed successfully. For this you can execute following command from terminal on Linux or cmd on Windows::

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
