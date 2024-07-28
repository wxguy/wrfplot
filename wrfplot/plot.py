#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Plot data on a Map """
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

import matplotlib.pyplot as plt
import os
from wrf import to_np, cartopy_xlim, cartopy_ylim, smooth2d
import cartopy
import numpy as np
from cartopy import feature as cf
from cartopy.feature import ShapelyFeature
from cartopy.io.shapereader import Reader
import cartopy.crs as ccrs
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.axes as maxes
from tqdm import tqdm
from matplotlib.colors import BoundaryNorm
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


class PlotMap(object):
    """Plot data on a map with necessary colours and title"""

    def __init__(
        self,
        var_name=None,
        u_level=None,
        clevels=False,
        fig_format="png",
        output_dir=None,
        dpi=150,
        config_file=None,
    ):
        super(PlotMap, self).__init__()
        self.var_name = var_name
        self.proj = None
        self.clevels = clevels
        self.ulevel = u_level
        self.fig = None
        self.ax = None
        self.grd_lns = None  # Grid lines
        self.cf = None  # Contour fill
        self.cs = None  # Contour line
        self.cl = None  # Contour label
        self.barbs = None
        self.fig_format = fig_format
        self.output_dir = output_dir
        self.dpi = dpi
        self.config = config_file
        self.c_bar_extend = None
        self.cbar = None
        self.cax = None
    
    def create_fig(self, projection):
        """Create Fig"""
        if self.proj is None:
            self.proj = projection
        if self.ax is None or self.fig is None:
            self.fig, self.ax = plt.subplots(
                figsize=(12, 8),
                subplot_kw=dict(projection=self.proj),
                frameon=True,
                num=1,
                clear=True,
            )
            self.add_shp_features()
            self.add_grids()

    def add_shp_features(self):
        """Read shapefile and add as cartopy features"""
        wld_shp_f = os.path.join(utils.data_dir(), "shape", "world_shape.shp")
        wld_shp_features = ShapelyFeature(Reader(wld_shp_f).geometries(), ccrs.PlateCarree(), facecolor="none")
        self.ax.add_feature(wld_shp_features, linewidth=0.5, edgecolor="black", alpha=0.7)

    def contour(self, var_name, lons, lats, data, title, clevels, fcst_time, colors='blue'):
        self.clear_plots()
        if var_name == "slp":
            data = smooth2d(data, 3, cenweight=4)
            self.cs = self.ax.contour(lons, lats, data, colors=colors, transform=ccrs.PlateCarree(), linewidths=1.0,
                                      levels=clevels)
        else:
            self.cs = self.ax.contour(lons, lats, data, colors="blue", transform=ccrs.PlateCarree(), linewidths=0.5, levels=self.clevels)

        self.cl = self.ax.clabel(self.cs, inline=1, fontsize=10, fmt="%1.0f", inline_spacing=1)
        self.plot_title(title)
        # self.set_xy_lim(data)

        return self.save_fig(var=var_name, fcst_time=fcst_time)

    def winds(self, var_name, lons, lats, u_data, v_data, wspd, title, clevels, colors, cmap, fcst_time, level=None):
        thin = utils.get_auto_resolution(to_np(lats))
        flip_array = (lats < 0)
        self.clear_plots()
        self.contour_fill(var_name=var_name, lons=lons[::thin, ::thin], lats=lats[::thin, ::thin],
                          data=wspd[::thin, ::thin] , title=title, clevels=clevels, colors=colors, cmap=cmap,
                          fcst_time=fcst_time)

        self.barbs = self.ax.barbs(to_np(lons)[::thin, ::thin], to_np(lats)[::thin, ::thin],
                                   to_np(u_data)[::thin, ::thin], to_np(v_data)[::thin, ::thin],
                                   transform=ccrs.PlateCarree(), length=5.5, sizes={"spacing": 0.2},
                                   pivot="middle", flip_barb=flip_array[::thin, ::thin])

        return self.save_fig(var=var_name, fcst_time=fcst_time, _level=level)

    def contour_fill(self, var_name, lons, lats, data, title, clevels, colors, cmap, fcst_time, level=None):
        if isinstance(clevels, int):
            bnorm = 'linear'
        else:
            bnorm = BoundaryNorm(clevels, cmap.N)
        if self.c_bar_extend is None:
            self.c_bar_extend = utils.get_cbar_extend(var_name)
        self.clear_plots()
        self.cf = self.ax.contourf(lons, lats, data, transform=ccrs.PlateCarree(), cmap=cmap, norm=bnorm,
                                   levels=clevels, extend=self.c_bar_extend)
        self.cs = self.ax.contour(self.cf, colors=colors, transform=ccrs.PlateCarree(), linewidths=0.3)
        self.cl = self.ax.clabel(self.cs, inline=1, fontsize=6, fmt="%1.0f", inline_spacing=1)

        self.plot_title(title)
        self.set_xy_lim(lons=lons, lats=lats)
        self.add_cbar(var_name=var_name, clevels=clevels)

        if var_name not in ['winds', 'u_winds']:
            return self.save_fig(var=var_name, fcst_time=fcst_time, _level=level)

    def plot_title(self, title_text=''): 
        self.ax.set_title(title_text, fontsize=12, weight="semibold", style="oblique", stretch="normal", family="serif")
    
    def add_cbar(self, var_name, clevels):
        """Plot colorbar next to plotted axes"""
        # 'neither', 'both', 'min', 'max'
        if self.c_bar_extend is None:
            self.c_bar_extend = self.config[var_name]["c_bar_extend"]

        if not self.cbar:
            # F = plt.gcf()
            divider = make_axes_locatable(self.ax)
            self.cax = divider.append_axes("right", size="3.0%", pad=0.2, axes_class=maxes.Axes)
            self.fig.add_axes(self.cax)
            self.cbar = plt.colorbar(self.cf, cax=self.cax, orientation="vertical", extend=self.c_bar_extend)
            unit = self.config[var_name]["unit"].replace('"', "")
            self.cbar.set_ticks(clevels)
            self.cbar.ax.tick_params(labelsize=8)
            self.cbar.set_label(label=unit, size="large", weight="bold")
            self.cbar.ax.text(0.5, 0, "", va="top", ha="center")

    def add_grids(self):
        """Add grid lines to plot"""
        self.grd_lns = self.ax.gridlines(
            draw_labels=True, color="gray", alpha=0.5, linestyle="--"
        )
        self.grd_lns.top_labels = False
        self.grd_lns.right_labels = False
    
    def set_xy_lim(self, lons, lats):
        self.ax.set_extent([np.min(lons), np.max(lons), np.min(lats), np.max(lats)], crs=ccrs.PlateCarree())
        """self.ax.set_ylim(cartopy_ylim(var_data))
        self.ax.set_xlim(cartopy_xlim(var_data))"""
        
    def save_fig(self, var, fcst_time, _level=None):
        """Save plotted image to local filesystem"""
        file_id = "%s_%s" % (var, fcst_time)
        if "u_" in var:
            file_id = "%s_%s_%s" % (var, _level, fcst_time)
        filename = "%s.%s" % (file_id.replace(" ", "_"), self.fig_format)
        # Windows fix
        # Widows does not accept file containing ":" in the file name. So replace it with '_'.
        filename = filename.replace(":", "_")
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        # plt.savefig(os.path.join(self.output_dir, filename), bbox_inches="tight", dpi=self.dpi)
        self.fig.savefig(os.path.join(self.output_dir, filename), bbox_inches="tight", dpi=self.dpi,
                         format='png')
        # self.clear_plots()
        if os.path.exists(os.path.join(self.output_dir, filename)):
            tqdm.write("\t  Image saved at : " + utils.quote(os.path.join(self.output_dir, filename)))

            return os.path.join(self.output_dir, filename)
        else:
            return None

    def clear_plots(self):
        try:
            if self.cs:
                self.cs.remove()
            if self.cf:
                self.cf.remove()
            if self.barbs:
                self.barbs.remove()
            if self.cax:
                self.cax.remove()
                self.cbar = False
            """if self.cbar:
                self.cbar.remove()
                self.cbar = False"""
        except Exception as e_clr_plt:
            #   print(e_clr_plt)
            pass

