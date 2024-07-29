## About wrfplot

`wrfplot` is a Command Line application written in Python Programming Language to plot set of diagnostic forecast variables from Weather Research and Forecasting (WRF) atmospheric model output file. Though, WRF model output files are simple NetCDF, it requires one to install various software and libraries to plot even a single variable. Python has many modules that can deal with WRF model output data set. However, setting up these libraries, plotting variables through reading a lot of documentation is a tedious process. wrfplot aims to fill this gap by proving an application that is easy to install and use.

The idea of developing `wrfplot` came to my mind as I frequently revisit the same code base again and again to tweak a few lines of code to get changes in final plots. Therefore, I was looking for a command line application that would help me to generate a common WRF model forecast images by providing appropriate command line options. I could not find any and hence created one.

## Use Cases

A typical use case of `wrfplot` would be to include as part of your WRF model run framework to plotting of variables immediately after the model run is completed. The other use case would be to use it for producing publication quality 2D maps that do not have much tweaking for your publication.

!!! note

    `wrfplot` is a new application. If you find any issues related to plotting variables or documentation, please open an issue in Github as given here Support


The best way to explore the application is to read and execute the extensive examples from Example Commands.

For complete list of options, execute the following command in the terminal or cmd window:

```console
$ wrfplot --help
```
