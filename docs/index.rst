.. wrfplot documentation master file, created by
   sphinx-quickstart on Tue Jul 26 20:03:56 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. image:: https://readthedocs.org/projects/wrfplot/badge/?version=latest
    :target: https://wrfplot.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

About wrfplot
===================================

**wrfplot** is a command line application written in Python programming language to plot set of diagnostic variables from World Research and Forecasting (WRF) atmospheric model output file. Though, WRF model output files are simple NetCDF, it requires one to install various software and libraries to plot a few variables.  Python has many modules that can deal with WRF model output data set. However, setting up theses libraries, plotting variables through reading lot of documentation is tedious process. **wrfplot** aims to fill this gap by proving an application that is easy to install and use. 

The idea of developing wrfplot came to my mind as I frequently revisit the same code base again and again to tweak few lines of code to get changes in final plots. Therefore, I was looking for a command line application that would help me to tweak the common WRF model forecast images by providing appropriate command line options. I could not find any and hence created one.

Use Cases
=========

A typical use case of wrfplot would be to include as part of your WRF model run framework to plotting of variables immediately after the model run is completed. The other use case would be to use it for producing publication quality 2D maps which does not much tweaking for your publication.

.. note::
  wrfplot is a new application. If you find any issues related to plotting variables or documentation, please open an issue in Github as given here :doc:`support`

The best way to explore the application is to read and execute the extensive examples from :doc:`examples`.

For complete list of options, execute following command in terminal or cmd window::

   $ wrfplot --help

.. toctree::
   :maxdepth: 2
   :hidden:
   
   install
   variables
   usage
   examples
   support
   contributing
   authors
   history
   modules


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
