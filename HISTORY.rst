=======
History
=======

v0.3.3 (2023-01-31)
------------------------
* Updated pyproject.toml to make use of "build" module (finding it much simpler to use)
* Fix for rub time versioning
* Removed setup.cfg file from source
* Removed versioneer as dependency

v0.3.2 (2023-01-31)
------------------------
Not released. Due to various internal bugs.

v0.3.1 (2023-01-30)
------------------------
* Shifted compilation backend to pyinstaller for automatic release process
* Fix for colormaps module to work with latest version of matplotlib
* Included versioneer for managing app version
* Fix for crash while including frameon parameter with latest version of matplotlib
* Refer the Documentation at https://wrfplot.readthedocs.io/

v0.2.7 (2022-09-07)
------------------------
* Cartopy no more would download shapefile from internet
* Fixed bug that caused plotting of upper atmospheric data to fail
* Added test script for automated testing
* No more crashes when plotting multiple variables (both surface and upper atmosphere data)
* Refer the Documentation at https://wrfplot.readthedocs.io/

v0.1.0 (2022-09-07)
------------------------
* Automated build process using GitHub actions
* Documentation now lives at https://wrfplot.readthedocs.io/

v0.1.0-beta (2022-08-30)
------------------------
* Fixed the pyproj database missing error.
* Include the Windows setup file. 
* Updated readme file to reflect installation procedures.
* Tweaked build script and included static images.
* Tweak to windows NSIS installer script to change the output name

v0.1.0-alpha (2022-08-27)
-------------------------
* First alpha release.
* Still a work in progress. 
* Pushing it to test the release-related aspects.
