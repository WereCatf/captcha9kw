# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import tomli
import os
import sys
sys.path.insert(0, os.path.abspath('../..'))
sys.path.insert(0, os.path.abspath('../../captcha9kw'))


# -- Project information -----------------------------------------------------

project = 'captcha9kw'
copyright = '2021, WereCatf'
author = 'WereCatf'

# The full version, including alpha/beta/rc tags
with open("../../pyproject.toml", "rb") as _:
    toml_dict = tomli.load(_)
    release = toml_dict["tool"]["poetry"]["version"]


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "cloud_sptheme",
    "sphinx.ext.autosummary",
    "sphinxcontrib.restbuilder",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "cloud"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
html_css_files = ["custom.css"]
autosummary_imported_members = True

html_sidebars = {"**": ["localtoc.html", "globaltoc.html",
                        "quicklinks.html", "searchbox.html"], }
html_theme_options = {
    "bodyfont": "\"Roboto\", sans-serif",
    "headfont": "\"Roboto\", serif",
    "fontcssurl": "https://fonts.googleapis.com/css?family=Roboto:400,i,b,bi|Open+Sans:400,i,b,bi|Roboto+Mono:400,i,b,bi&display=swap",
}
