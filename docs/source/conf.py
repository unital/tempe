# SPDX-FileCopyrightText: 2024-present Unital Software <info@unital.dev>
#
# SPDX-License-Identifier: MIT

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Tempe'
copyright = '2024, Unital Software'
author = 'Unital Software'
release = '0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.napoleon',
    'autoapi.extension',
    "sphinx_design",
]

templates_path = ['_templates']
exclude_patterns = []

# -- Options for intersphinx -------------------------------------------------

intersphinx_mapping = {
    'micropython': ('https://docs.micropython.org/en/latest', None),
    'python': ('https://docs.python.org/3', None)
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'pydata_sphinx_theme'
html_static_path = ['_static']
html_theme_options = {
    "use_edit_page_button": True,
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/unital/tempe",
            "icon": "fa-brands fa-github",
            "type": "fontawesome",
        },
        {
            "name": "Unital",
            "url": "https://www.unital.dev",
            "icon": "_static/logo-dark.svg",
            "type": "local",
        },
    ],
    "icon_links_label": "Quick Links",
}
html_context = {
    "github_user": "unital",
    "github_repo": "tempe",
    "github_version": "main",
    "doc_path": "docs",
    "default_mode": "dark",
}

# -- Options for autodoc -----------------------------------------------------
import sys
import os
sys.path.insert(0, os.path.abspath('../../src'))  # add my lib modules

autodoc_mock_imports = [
    'machine',
    'uasyncio',
    'utime',
    'framebuf',
]
autosummary_generate = True

# -- Options for autoapi -----------------------------------------------------
autoapi_dirs = ['../../src']
autoapi_root = 'api'
autoapi_file_patterns = ['*.pyi', '*.py']
autoapi_options = [
    'members',
    'undoc-members',
    'private-members',
    'show-inheritance',
    'show-module-summary',
    'imported-members',
]
autoapi_ignore = ["*_data_view_math*"]

add_module_names = False
python_maximum_signature_line_length = 60