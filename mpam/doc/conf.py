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
sys.path.insert(0, os.path.abspath('../src'))


# -- Project information -----------------------------------------------------

project = 'MPAM'
copyright = '2022, Evan Kirshenbaum'
author = 'Evan Kirshenbaum'

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx_toolbox.decorators',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon',
]

autosummary_generate = True

autodoc_default_options = {
    "members": True,
    # "imported-members": True,
    "show-inheritance": True,
    "recursive": True,
    # "exclude-members": "__init__",
    "special-members": ",".join([
                                "__init__", "__call__",
                                "__get__",  "__set__", "__delete__",
                                "__getitem__"
                            ]),
    # "special-members": "__init__,__call__,__get__,__set__,__getitem__",
    # "private-members": True,
    # "special-members": True,
    # "inherited-members": True,
    
}

# autodoc_typehints = "both"
autodoc_typehints_format = "short"

# On the one hand, adding type aliases makes the documentation more readable. On
# the other hand, it doesn't emit links to the aliases, so if you don't know
# what they are, you have to seach for them.
autodoc_type_aliases = {
    # "DelayType": "mpam.types.DelayType",
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'haiku' # 'alabaster'
# html_theme = "alabaster"
html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

html_css_files = [
    "theme_overrides.css"
]
