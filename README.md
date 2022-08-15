## About wrfplot

**wrfplot** is a command line application written in Python programming language to plot set of diagnostic variables from World Research and Forecasting (WRF) atmospheric model output file. Though, WRF model output files are simple NetCDF, it requires one to install various software and libraries to plot a few variables.  Python has many modules that can deal with WRF model output data set. However, setting up theses libraries, plotting variables through reading lot of documentation is tedious process. **wrfplot** aims to fill this gap by proving an application that is easy to install and use. 

The idea of developing wrfplot came to my mind as I frequently revisit the same code base again and again to tweak few lines of code to get changes in final plots. Therefore, decided to start this project where most of the common visualisation can be tweaked by providing appropriate command line options.

## Use Cases

A typical use case of wrfplot would be to include as part of your WRF model run framework to plotting of variables immediately after the model run is completed. The other use case would be to use it for producing publication quality 2D maps which does not much tweaking for your publication.

