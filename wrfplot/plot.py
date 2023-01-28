#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Plot data on a Map """
"""
This file is part of wrfplot application.

wrfplot is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

wrfplot is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with wrfplot. If not, see <http://www.gnu.org/licenses/>.
"""

__author__ = "J Sundar (wrf.guy@gmail.com)"

import matplotlib.pyplot as plt
import os
from wrf import to_np
import cartopy
from cartopy import feature as cf
from cartopy.feature import ShapelyFeature
from cartopy.io.shapereader import Reader
import cartopy.crs as ccrs
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.axes as maxes
from tqdm import tqdm
from matplotlib.colors import BoundaryNorm
import json
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import utils
import warnings
from shapely.errors import ShapelyDeprecationWarning

warnings.filterwarnings("ignore", category=ShapelyDeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)
# For debugging purpose
# print(utils.data_dir())
# print(cartopy.config['data_dir'])

# Set the cartopy NE shape file to our data dir
cartopy.config["pre_existing_data_dir"] = os.path.abspath(utils.data_dir())


class MakePlot(object):
    """Plot data on a map with necessary colours and title"""

    def __init__(
        self,
        var_name=None,
        data=None,
        u_kt=None,
        v_kt=None,
        lons=None,
        lats=None,
        run_time=None,
        fcst_hr=None,
        u_level=None,
        proj=None,
        cmap=None,
        clevels=None,
        fig_format="png",
        output_dir=None,
        dpi=150,
        config_file=None,
    ):
        super(MakePlot, self).__init__()
        self.var_name = var_name
        self.data = data
        self.U = u_kt
        self.V = v_kt
        self.lons = lons
        self.lats = lats
        self.proj = proj
        self.clevels = clevels
        self.cycle = run_time
        self.fcst_hr = fcst_hr
        self.ulevel = u_level
        self.cmap = cmap
        self.fig = None
        self.ax = None
        self.grd_lns = None  # Grid lines
        self.cf = None  # Contour fill
        self.cs = None  # Contour line
        self.cl = None  # Contour label
        self.fig_format = fig_format
        self.output_dir = output_dir
        self.dpi = dpi
        self.config = config_file
        self.c_bar_extend = self.config.get(self.var_name, "c_bar_extend").replace(
            '"', ""
        )

    def create_fig(self):
        """Create Fig"""
        if self.ax is not None or self.fig is None:
            self.fig, self.ax = plt.subplots(
                figsize=(12, 8),
                subplot_kw=dict(projection=self.proj),
                frameon=True,
                num=1,
                clear=True,
            )

    def add_shp_features(self):
        """Read shapefile and add as cartopy features"""
        wld_shp_f = os.path.join(utils.data_dir(), "shape", "world_shape.shp")
        wld_shp_features = ShapelyFeature(
            Reader(wld_shp_f).geometries(), ccrs.PlateCarree(), facecolor="none"
        )
        self.ax.add_feature(
            wld_shp_features, linewidth=0.5, edgecolor="black", alpha=0.7
        )
        # self.ax.add_feature(cartopy.feature.LAND)

    def add_background(self):
        """Add stock image to plot axex"""
        self.ax.stock_image()

    def add_cartopy_features(self):
        """Add cartopy features only for specific variables"""
        if self.var_name in ["slp", "mslp"]:
            self.ax.add_feature(cf.LAND)
            self.ax.add_feature(cf.OCEAN)

    def add_grids(self):
        """Add grid lines to plot"""
        self.grd_lns = self.ax.gridlines(
            draw_labels=True, color="gray", alpha=0.5, linestyle="--"
        )
        self.grd_lns.xlabels_top = False
        self.grd_lns.ylabels_right = False
        self.grd_lns.xformatter = LONGITUDE_FORMATTER
        self.grd_lns.yformatter = LATITUDE_FORMATTER

    def plot_var(self):
        """Main function to call other mehtods to plot variable"""
        if self.fig is None:
            self.create_fig()
            self.add_shp_features()
            self.add_cartopy_features()

        # self.add_background()
        self.add_grids()
        self.get_cmap()
        self.get_clevels()
        self.plot_data()
        self.plot_title()
        if not self.var_name == "slp":
            self.plot_cbar()
        self.save_fig()

    def get_clevels(self):
        """Get contour levels"""
        if self.clevels == "auto":
            self.clevels = utils.get_auto_clevel(self.data)

    def plot_title(self):
        """Plot title for the given variable"""
        title = json.loads(self.config.get(self.var_name, "title"))
        unit = self.config.get(self.var_name, "unit").replace('"', "")
        if self.ulevel is not None:
            title_text = (
                title
                + " ("
                + unit
                + ") at "
                + str(self.ulevel)
                + " hPa\nModel Run Hr : "
                + self.cycle
                + " UTC  |  Fcst Hr : "
                + self.fcst_hr
                + " UTC"
            )
        else:
            title_text = (
                title
                + " ("
                + unit
                + ")\nModel Run Hr : "
                + self.cycle
                + " UTC  |  Fcst Hr : "
                + self.fcst_hr
                + " UTC"
            )
        self.ax.set_title(
            title_text,
            fontsize=12,
            weight="semibold",
            style="oblique",
            stretch="normal",
            family="serif",
        )

    def get_cmap(self):
        """Get cmap from variable.ini file"""
        cmap_name = "None"
        if self.cmap is not None:
            self.cmap = utils.get_cmap(self.cmap)
        else:
            cmap_name = json.loads(self.config.get(self.var_name, "cmap"))
        if cmap_name == "None":
            self.cmap = None
        else:
            self.cmap = utils.get_cmap(cmap_name)

    def plot_cbar(self):
        """Plot colorbar next to plotted axes"""
        # 'neither', 'both', 'min', 'max'
        F = plt.gcf()
        divider = make_axes_locatable(self.ax)
        cax = divider.append_axes("right", size="3.0%", pad=0.2, axes_class=maxes.Axes)
        F.add_axes(cax)
        bar = plt.colorbar(
            self.cf, cax=cax, orientation="vertical", extend=self.c_bar_extend
        )
        unit = self.config.get(self.var_name, "unit").replace('"', "")
        bar.set_ticks(self.clevels)
        bar.ax.tick_params(labelsize=8)
        bar.set_label(label=unit, size="large", weight="bold")
        bar.ax.text(0.5, 0, "", va="top", ha="center")

    def plot_data(self):
        """Plot 2D data on a Map"""
        # We need to normalise the colour map with data levels. Otherwise, colourmap will be squed
        # SLP data does not reqire to have colour fill
        if self.var_name == "slp":
            self.cs = plt.contour(
                self.lons,
                self.lats,
                self.data,
                colors="blue",
                transform=ccrs.PlateCarree(),
                linewidths=0.5,
                levels=self.clevels,
            )
            self.cl = plt.clabel(
                self.cs, inline=1, fontsize=10, fmt="%1.0f", inline_spacing=1
            )
        else:
            norm = BoundaryNorm(self.clevels, self.cmap.N)
            self.cf = self.ax.contourf(
                self.lons,
                self.lats,
                self.data,
                transform=ccrs.PlateCarree(),
                cmap=self.cmap,
                norm=norm,
                levels=self.clevels,
                extend=self.c_bar_extend,
            )  # colors=('lime', 'limegreen', 'darkgreen', 'yellow', 'orange', 'red', 'purple')
            self.cs = self.ax.contour(
                self.cf, colors="black", transform=ccrs.PlateCarree(), linewidths=0.3
            )
            self.cl = self.ax.clabel(
                self.cs, inline=1, fontsize=6, fmt="%1.0f", inline_spacing=1
            )

        # Plot wind barbs on top of contourf only if U and V components are available
        if self.U is not None and self.V is not None:
            """print(self.lats)
            print(self.lons)
            print(self.U)
            print(self.V)
            sys.exit()"""
            thin = utils.get_auto_resolution(to_np(self.lats))
            self.ax.barbs(
                to_np(self.lons)[::thin, ::thin],
                to_np(self.lats)[::thin, ::thin],
                to_np(self.U)[::thin, ::thin],
                to_np(self.V)[::thin, ::thin],
                transform=ccrs.PlateCarree(),
                length=5.5,
                sizes={"spacing": 0.2},
                pivot="middle",
            )

    def save_fig(self):
        """Save plotted image to local filesystem"""
        file_id = "%s_%s" % (self.var_name, self.fcst_hr)
        if "u_" in self.var_name:
            file_id = "%s_%s_%s" % (self.var_name, self.ulevel, self.fcst_hr)
        filename = "%s.%s" % (file_id.replace(" ", "_"), self.fig_format)
        # Windows fix
        # Widows does not accept file containing ":" in the file name. So replace it with '_'.
        filename = filename.replace(":", "_")
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        plt.savefig(
            os.path.join(self.output_dir, filename),
            bbox_inches="tight",
            dpi=self.dpi,
            frameon=True,
        )
        if os.path.exists(os.path.join(self.output_dir, filename)):
            tqdm.write(
                "\t  Image saved at : "
                + utils.quote(os.path.join(self.output_dir, filename))
            )
        self.fig.canvas.flush_events()
        plt.close()

    def animation(self, input_dir, variable, level=False, speed=0.5, loop=0):
        """
        Make animation for variable
        # TODO
        """
        print("")
