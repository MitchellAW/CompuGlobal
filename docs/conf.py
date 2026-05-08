# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "compuglobal"
copyright = "2018, MitchellAW"
author = "MitchellAW"
release = "0.3.0"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinxcontrib_trio",
    "enum_tools.autoenum",
    "sphinx_rtd_theme",
]

autodoc_member_order = "bysource"
autodoc_typehints = "none"
autodoc_preserve_defaults = False
add_module_names = True
autoclass_content = "class"

napoleon_use_google_docstring = False
napoleon_use_param = False
napoleon_use_ivar = True
napoleon_attr_annotations = False

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_theme_options = {"navigation_depth": 3}
html_static_path = ["_static"]
