# (C) Copyright 2007-2021 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

# This file is execfile()d with the current directory set to its containing
# dir.
#
# The contents of this file are pickled, so don't put values in the namespace
# that aren't pickleable (module imports are okay, they're removed
# automatically).
#
# All configuration values have a default value; values that are commented out
# serve to show the default value.

import envisage
import enthought_sphinx_theme

# If your extensions are in another directory, add it here. If the directory
# is relative to the documentation root, use os.path.abspath to make it
# absolute, like shown here.
# sys.path.append(os.path.abspath('some/directory'))

# General configuration
# ---------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.extlinks",
    "sphinx.ext.githubpages",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "traits.util.trait_documenter",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix of source filenames.
source_suffix = ".rst"

# The master toctree document.
master_doc = "index"

# General substitutions.
project = "envisage"
copyright = "2008-2021, Enthought"

# The default replacements for |version| and |release|, also used in various
# other places throughout the built documents.
version = release = envisage.__version__

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
# today = ''
# Else, today_fmt is used as the format for a strftime call.
today_fmt = "%B %d, %Y"

# List of documents that shouldn't be included in the build.
# unused_docs = []

# List of directories, relative to source directories, that shouldn't be
# searched for source files.
# exclude_dirs = []

# The reST default role (used for this markup: `text`) to use for all
# documents.
# default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
# add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
# add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
# show_authors = False

# Substitutions reusable for all files.

rst_epilog = """
..
   # substitutions for API objects

.. |Application| replace:: :class:`~envisage.application.Application`
.. |IApplication| replace:: :class:`~envisage.i_application.IApplication`
.. |ExtensionPoint| replace:: :class:`~envisage.extension_point.ExtensionPoint`
.. |Plugin| replace:: :class:`~envisage.plugin.Plugin`
.. |IPlugin| replace:: :class:`~envisage.i_plugin.IPlugin`
.. |envisage.api| replace:: :mod:`envisage.api`
.. |envisage.ui.workbench| replace:: :mod:`envisage.ui.workbench.api`

..
   # substitutions for the Hello World example

.. |Hello World| replace:: :github-demo:`Hello World <Hello_World/hello_world.py>`

..
   # substitutions for MOTD examples

.. |acme.motd| replace:: :github-demo:`acme.motd <MOTD/acme/motd/motd_plugin.py>`
.. |acme.motd.software_quotes| replace:: :github-demo:`acme.motd.software_quotes <MOTD/acme/motd/software_quotes/software_quotes_plugin.py>`
.. |MOTD| replace:: :github-demo:`MOTD <MOTD/acme/motd/motd.py>`
.. |IMOTD| replace:: :github-demo:`IMOTD <MOTD/acme/motd/i_motd.py>`
.. |MOTDPlugin| replace:: :github-demo:`MOTDPlugin <MOTD/acme/motd/motd_plugin.py>`
.. |MOTD run| replace:: :github-demo:`run.py <MOTD/run.py>`
.. |IMessage| replace:: :github-demo:`IMessage <MOTD/acme/motd/i_message.py>`
.. |Message| replace:: :github-demo:`Message <MOTD/acme/motd/message.py>`
.. |messages.py| replace:: :github-demo:`message.py <MOTD/acme/motd/software_quotes/messages.py>`
.. |Message of the Day| replace:: :github-demo:`Message of the Day <MOTD>`
"""   # noqa: E501

# Options for HTML output
# -----------------------

# Use the Enthought Sphinx Theme (see
# https://github.com/enthought/enthought-sphinx-theme)
html_theme_path = [enthought_sphinx_theme.theme_path]
html_theme = "enthought"

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
html_title = "Envisage Documentation"

# A shorter title for the navigation bar.  Default is the same as html_title.
# html_short_title = None

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = []

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
html_last_updated_fmt = "%b %d, %Y"

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
# html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.
# html_additional_pages = {}

# If false, no module index is generated.
html_use_modindex = False

# If false, no index is generated.
# html_use_index = True

# If true, the index is split into individual pages for each letter.
# html_split_index = False

# If true, the reST sources are included in the HTML build as _sources/<name>.
# html_copy_source = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
# html_use_opensearch = ''

# If nonempty, this is the file name suffix for HTML files (e.g. ".xhtml").
# html_file_suffix = ''

# Output file base name for HTML help builder.
htmlhelp_basename = "Envisagedoc"


# Options for LaTeX output
# ------------------------

# The paper size ('letter' or 'a4').
# latex_paper_size = 'letter'

# The font size ('10pt', '11pt' or '12pt').
# latex_font_size = '10pt'

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, document class
# [howto/manual]).
latex_documents = [
    (
        "index",
        "Envisage.tex",
        "Envisage Documentation",
        "Enthought, Inc.",
        "manual",
    ),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
# latex_logo = "enthought_logo.jpg"
latex_logo = "e-logo-rev.png"

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
# latex_use_parts = False

# Additional stuff for the LaTeX preamble.
# latex_preamble = ''

# Documents to append as an appendix to all manuals.
# latex_appendices = []

# If false, no module index is generated.
# latex_use_modindex = True

# -- Options for intersphinx extension ---------------------------------------

intersphinx_mapping = {
    "pyface": ("https://docs.enthought.com/pyface", None),
    "python": ("https://docs.python.org/3", None),
    "traits": ("https://docs.enthought.com/traits", None),
    "traitsui": ("https://docs.enthought.com/traitsui", None),
}


# -- Options for extlinks extension -------------------------------------------

extlinks = {
    'github-demo': (
        'https://github.com/enthought/envisage/tree/main/envisage/examples/demo/%s',   # noqa: E501
        '')
}
