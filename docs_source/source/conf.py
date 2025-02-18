# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup -----------------------------------------------------
import os
import sys

sys.path.insert(0, os.path.abspath("../../datamesh_checker"))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Starburst Data Product Checker'
copyright = '2024, Gougou Nelson'
author = 'Gougou Nelson'
release = '0.5.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.githubpages",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
]

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# -- Options for autodoc ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html
autoclass_content = "both"