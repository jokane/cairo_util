# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import sys
import os
import subprocess

sys.path.insert(0, os.path.join(os.path.split(__file__)[0], '..'))
sys.path.insert(0, os.path.join(os.path.split(__file__)[0], '.'))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'cairo_util'
copyright = "2025, Jason O'Kane"
author = "Jason O'Kane"

version_filename = os.path.join(os.path.split(__file__)[0], "../cairo_util/version.py")
with open(version_filename) as version_file:
    exec(compile(version_file.read(), version_filename, "exec"))
version = version_from_git()

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc',
              'sphinx_rtd_theme']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', '_generated']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_theme_options = {'collapse_navigation': False,
                       'navigation_depth': 1,
                      'prev_next_buttons_location': None }
html_static_path = []

autodoc_member_order = 'bysource'
