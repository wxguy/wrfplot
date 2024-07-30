#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" wrfplot entry point to the application """
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
import sys
import fileio
import argparse
import arguments
import wrf
import timeit
from importlib.metadata import version
from core import WrfPlot
import traceback


# Set these env variables to avoid font related errors
os.environ["FONTCONFIG_PATH"] = "$CONDA_PREFIX/etc/fonts/"
os.environ["FONTCONFIG_FILE"] = "$CONDA_PREFIX/etc/fonts/fonts.conf"
# Have to set update env variables before importing pyproj module when running from freeze mode
custom_pyproj_dbase_dir = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "pyproj", "proj"
)
if os.path.exists(custom_pyproj_dbase_dir):
    os.environ["PROJ_LIB"] = custom_pyproj_dbase_dir
    os.environ["PATH"] += os.pathsep + custom_pyproj_dbase_dir
    os.environ["PATH"] += os.path.dirname(os.path.abspath(__file__))


VERSION = 'unknown'

try:
    __version__ = version("wrfplot")
except:
    # package is not installed
    # Get the version from the local file
    import _version
    __version__ = _version.__version__
finally:
    # Do nothing
    pass

# Enable cartopy using wrf moudule's inbuilt method
wrf.enable_cartopy()


def arg_praser():
    """Form command line input"""
    prog_name = (
        "Command line application to plot static WRF model prognostic products..."
    )
    parser = argparse.ArgumentParser(
        description=prog_name, epilog="\u00a9 J Sundar, wrf.guy@gmail.com, 2024"
    )
    parser.add_argument(
        "--list-vars", action="store_true", help="Show list of variables supported by wrfplot and exit."
    )
    parser.add_argument(
        "--input",
        metavar="<input_file>",
        type=arguments.file_path,
        help="Path to WRF generated netCDF.",
    )
    parser.add_argument(
        "--output",
        metavar="<output_dir>",
        type=arguments.dir_path,
        default=False,
        help="Path to output directory for saving plotted images.",
    )
    parser.add_argument(
        "--vars",
        metavar="<variable(s)>",
        type=arguments.validate_vars,
        help="Name of the variable to be plotted. Multiple variables are to be separated with ','. Use '--list-vars' "
             "option to see list of supported variables.",
    )
    parser.add_argument(
        "--ulevels",
        metavar="<upper-levels>",
        type=arguments.validate_ulevels,
        help="Provide custom upper level(s) when plotting upper atmospheric data. Each level is to be separated by ',' "
             "i.e., '925,850,700'. Use '--list-vars' to know list of supported upper level variables.",
    )
    parser.add_argument(
        "--list-cmaps",
        action="store_true",
        help="List colour maps (cmaps) supported by wrfplot. Refer https://pratiman-91.github.io/colormaps for "
             "information on each colourmaps.",
    )
    parser.add_argument(
        "--cmap",
        metavar="<cmap-name>",
        type=arguments.validate_cmap,
        default=False,
        help="Valid colormap name to fill colors. Use '--list-cmaps' option to see list of supported colormaps. Must "
             "have minimum 11 colors, else will lead to error.",
    )
    parser.add_argument(
        "--clevels",
        metavar="<contour-levels>",
        type=arguments.validate_clevels,
        default=False,
        help="Provide custom contour level(s) to highlight data. Levels are to be in ascending order and separated "
             "by ',' i.e., '24,26,28'. If single value is provided, clevels will be automatically calculated.",
    )
    parser.add_argument(
        "--dpi",
        metavar="<value>",
        type=int,
        help="Increase or decrease the plotted image resolution. Default is 125. More is higher resolution and less is "
             "course resolution. Higher values will reduce the speed of plot.",
    )
    parser.add_argument(
        "--gif",
        action="store_true",
        default=False,
        help="If applied, creates an animated GIF image. GIF image will be saved same location as other images with a "
             "name specifed in '--vars' option."
    )
    parser.add_argument(
        "--gif-speed",
        metavar="<seconds>",
        type=arguments.validate_gif_speed,
        default=False,
        help="Set speed of GIF frame in seconds. Default is 0.5 sec. Lower value increases the speed of animation. To "
             "be used with '--gif' option to take effect."
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="Print version information of 'wrfplot' and exit.",
    )
    return parser.parse_args()


def main():
    args = arg_praser()
    if args.list_vars:
        sys.exit(arguments.list_vars())
    elif args.list_cmaps:
        sys.exit(arguments.list_cmaps())
    elif args.version:
        sys.exit(print(__version__))
    elif not all([args.input, args.vars, args.output]):
        sys.exit(
            "You must provide path to WRF model output file using '--input' option, output directory for saving image "
            "files using '--output' option and must provide at least one variable name using '--vars' option to "
            "process.\nTypical usage will be \"wrfplot --input filename' --output 'path/to/output/dir' --vars 'slp'\""
        )
    elif all([args.input, args.vars, args.output]):
        file = fileio.FileIO(args.input)
        if file.is_wrf():
            # start_time = time.monotonic()
            start_time = timeit.default_timer()
            wrfplt = WrfPlot(
                input_path=args.input, output_path=args.output, dpi=args.dpi, cmap=args.cmap, ulevels=args.ulevels, animation=args.gif,
                animation_speed=args.gif_speed, clevels=args.clevels
            )
            try:
                wrfplt.read_file(args.input)
                if isinstance(args.vars, list):
                    wrfplt.total_vars = len(args.vars)
                    for var in args.vars:
                        wrfplt.set_variable(var)
                        wrfplt.plot.create_fig(wrfplt.proj)
                        wrfplt.plot_variable(var_name=var)
                else:
                    wrfplt.set_variable(args.vars)
                    wrfplt.plot.create_fig(wrfplt.proj)
                    wrfplt.plot_variable(var_name=args.vars)
                total_time = timeit.default_timer() - start_time
                mins, secs = divmod(total_time, 60)
                hours, mins = divmod(mins, 60)
                print(f"\nPlotting process completed. It took %dH:%dM:%fS\n" % (hours, mins, secs))
            except Exception as e:
                # print(e)
                print(traceback.format_exc())
                print("Failed to plot one or some variables...")


if __name__ == "__main__":
    main()
