
"""
This file is part of wrfplot cli application.

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

# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import os
import sys
import sphinx_rtd_theme  # must install through pip
sys.path.insert(0, os.path.abspath('..'))  # to ensure that our main application module is discoverable
from wrfplot._version import __version__


# The master toctree document.
master_doc = 'index'

# -- Project information -----------------------------------------------------

project = 'wrfplot'
copyright = '2022, WxGuy'
author = 'wxguy'

# The full version, including alpha/beta/rc tags
release = '0.1.0'


# The short X.Y version.
version = __version__
# The full version, including alpha/beta/rc tags.
release = __version__


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.autodoc',
              'sphinx.ext.viewcode',
              'sphinx.ext.napoleon',
              'sphinx.ext.autosummary',
              'sphinx.ext.imgconverter',
              'sphinx.ext.intersphinx',
              'sphinx.ext.mathjax']


# Turn off code and image links for embedded mpl plots
plot_html_show_source_link = False
plot_html_show_formats = False

# Tweak how docs are formatted
napoleon_use_rtype = False
napoleon_include_private_with_doc = False

# Control main class documentation
autoclass_content = 'both'

# source_suffix = ['.rst', '.md']
source_suffix = {'.rst': 'restructuredtext'}

# Controlling automatically generating summary tables in the docs
autosummary_generate = True
autosummary_imported_members = True

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

mathjax3_config = {'chtml': {'displayAlign': 'left'}}

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.

html_theme = 'sphinx_rtd_theme'

html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

html_theme_options = {'display_version': True,
                      'prev_next_buttons_location': 'bottom',
                      'includehidden': True
                      }

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
html_logo = os.path.join('_static', 'wrfplot.png')


# --------------- autosummary -------------------------------------------------

napoleon_custom_sections = [('Other Parameters', 'params_style')]

latex_documents = [('index', 'wrfplot.tex', u'wrfplot Documentation', u'J Sundar', 'manual'), ]
