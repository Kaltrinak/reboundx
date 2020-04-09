#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# REBOUNDx documentation build configuration file, created by
# sphinx-quickstart on Sun Nov 29 14:22:27 2015.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

import sys
import os
import shlex
import subprocess
import glob
import re
from datetime import datetime

# Doxygen trigger
read_the_docs_build = os.environ.get('READTHEDOCS', None) == 'True'
if read_the_docs_build:
    subprocess.call('cd doxygen; doxygen', shell=True)

# C Example update
with open("c_examples.rst","w") as fd:
    fd.write(".. _c_examples:\n\n")
    fd.write("Examples (C)\n")
    fd.write("============\n\n")
    for problemc in glob.glob("../examples/*/problem.c"):
        will_output = 0
        with open(problemc) as pf:
            fd.write(".. _c_example_{0}:\n\n".format(problemc.split('/', 2)[-1].split('/',1)[0])) # make a label c_example_name_of_effect for cross-referencing
            did_output=0
            empty_lines = 0
            for line in pf:
                if line[0:3] == "/**":
                    will_output += 1
                if line[0:3] == " */":
                    will_output = -1
                    line = ""
                    fd.write("\n\n.. code-block:: c\n");
                if will_output>1:
                    if will_output == 2:
                        under = "-"*(len(line.strip())-2)
                        line = "  " +line.strip() + '\n' + under
                    will_output = 2
                    if len(line[3:].strip())==0:
                        fd.write("\n\n"+line[3:].strip())
                    else:
                        fd.write(line[3:].strip() + " " )
                if will_output==-1:
                    fd.write("   " +line.rstrip() + "\n" )
                    did_output = 1
                if will_output>0:
                    will_output += 1
            fd.write("\n\nThis example is located in the directory `examples/"+problemc.split("/")[2]+"`\n\n")
            if did_output==0:
                print "Warning: Did not find description in "+problemc

# Update effects.rst
def cleanline(line):
    if line[3:] == "":
        return "\n"
    else:
        return line[3:]

sources = [each for each in os.listdir('../src') if each.endswith('.c')]
sources = [source[:-2] for source in sources] # all filenames ending with .c with the .c removed

with open("effects.rst", "w") as f:
    with open("effect_headers.txt", "r") as fh:
        lines = fh.readlines()
        i=0
        while i < len(lines):
            if lines[i].startswith(".. #"):
                i += 1    # skip comment line
            else:
                if "$$$" in lines[i]: # New category
                    i += 1
                    while lines[i].strip() == "": # skip white lines
                        i += 1
                    category = lines[i] # store category
                    while i < len(lines) and "$$$" not in lines[i]: # print category description
                        f.writelines(lines[i])
                        i += 1
                       
                    for source in sources:
                        with open("../src/" + source + ".c", "r") as fs: # search sources that match category
                            sourcelines = fs.readlines()
                            j=0
                            while "#include" not in sourcelines[j]:
                                if "$$$" in sourcelines[j]: # start of documentation block
                                    j += 1
                                    while sourcelines[j].strip() == "*": # skip empty lines
                                        j += 1
                                    res = re.search(r'\$(.*)\$', cleanline(sourcelines[j])) # search for category between dollar signs
                                    if res is not None:
                                        cat = res.group(1)
                                        if cat.strip().lower() == category.strip().lower(): # source is in category, need to document
                                            j += 1
                                            f.write(".. _"+source+":\n\n") # write tag
                                            f.write(source+"\n") # write implementation heading
                                            for k in range(len(source)):
                                                f.write("*")
                                            f.write("\n")
                                            while " */" not in sourcelines[j]:
                                                f.write(cleanline(sourcelines[j]))
                                                j += 1
                                            f.write("\n")
                                        else: # category doesn't match
                                           break
                                    else: # first non-empty line doesn't have category
                                        break
                                else:
                                    j += 1
                                
                else:
                    f.writelines(lines[i])
                    i += 1

        # Now document sources that had no category included separately
        for source in sources:
            with open("../src/" + source + ".c", "r") as fs: # search sources that match category
                sourcelines = fs.readlines()
                j=0
                while "#include" not in sourcelines[j]:
                    if "$$$" in sourcelines[j]: # start of documentation block
                        j += 1
                        while sourcelines[j].strip() == "*": # skip empty lines
                            j += 1
                        res = re.search(r'\$(.*)\$', cleanline(sourcelines[j])) # search for category between dollar signs
                        if res is None: # only document if no category present
                            f.write(source+"\n") # write section heading
                            for k in range(len(source)):
                                f.write("^")
                            f.write("\n\n")
                            f.write(".. _"+source+":\n\n") # write tag
                            f.write(source+"\n") # write implementation heading
                            for k in range(len(source)):
                                f.write("*")
                            f.write("\n\n")
                            while " */" not in sourcelines[j]:
                                f.write(cleanline(sourcelines[j]))
                                j += 1
                            break
                            f.write("\n")
                        else: # had category, don't document
                            break
                    else:
                        j += 1


# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#sys.path.insert(0, os.path.abspath('.'))

# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'breathe',
]
releases_github_path = "dtamayo/reboundx"
breathe_projects = { "libreboundx": "doxygen/xml/" }
breathe_default_project = "libreboundx"

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The encoding of source files.
#source_encoding = 'utf-8-sig'

# The master toctree document.
master_doc = 'index'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = '3.0'
# The full version, including alpha/beta/rc tags.
release = '3.0.5'

# General information about the project.
project = u"REBOUNDx ({0})".format(release)
year = datetime.now().year
author = 'Dan Tamayo, Hanno Rein'
copyright = u"{0} {1}".format(year, author)

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
#today = ''
# Else, today_fmt is used as the format for a strftime call.
#today_fmt = '%B %d, %Y'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['_build']

# The reST default role (used for this markup: `text`) to use for all
# documents.
#default_role = None

# If true, '()' will be appended to :func: etc. cross-reference text.
#add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
#add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
#show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# A list of ignored prefixes for module index sorting.
#modindex_common_prefix = []

# If true, keep warnings as "system message" paragraphs in the built documents.
#keep_warnings = False

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'alabaster'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
html_theme_options = {
    "description": "A library for additional effects in REBOUND N-body integrations",
    "github_user": "dtamayo",
    "github_repo": "reboundx",
}

# Add any paths that contain custom themes here, relative to this directory.
#html_theme_path = []

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
#html_title = None

# A shorter title for the navigation bar.  Default is the same as html_title.
#html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
#html_logo = None

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
#html_favicon = None

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Add any extra paths that contain custom files (such as robots.txt or
# .htaccess) here, relative to this directory. These files are copied
# directly to the root of the documentation.
#html_extra_path = []

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
#html_last_updated_fmt = '%b %d, %Y'

# If true, SmartyPants will be used to convert quotes and dashes to
# typographically correct entities.
#html_use_smartypants = True

# Custom sidebar templates, maps document names to template names.
#html_sidebars = {}
html_sidebars = {
                '**': ['about.html', 'navigation.html', 'relations.html', 'searchbox.html']
                }

# Additional templates that should be rendered to pages, maps page names to
# template names.
#html_additional_pages = {}

# If false, no module index is generated.
#html_domain_indices = True

# If false, no index is generated.
#html_use_index = True

# If true, the index is split into individual pages for each letter.
#html_split_index = False

# If true, links to the reST sources are added to the pages.
#html_show_sourcelink = True

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
#html_show_sphinx = True

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
#html_show_copyright = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
#html_use_opensearch = ''

# This is the file name suffix for HTML files (e.g. ".xhtml").
#html_file_suffix = None

# Language to be used for generating the HTML full-text search index.
# Sphinx supports the following languages:
#   'da', 'de', 'en', 'es', 'fi', 'fr', 'h', 'it', 'ja'
#   'nl', 'no', 'pt', 'ro', 'r', 'sv', 'tr'
#html_search_language = 'en'

# A dictionary with options for the search language support, empty by default.
# Now only 'ja' uses this config value
#html_search_options = {'type': 'default'}

# The name of a javascript file (relative to the configuration directory) that
# implements a search results scorer. If empty, the default will be used.
#html_search_scorer = 'scorer.js'

# Output file base name for HTML help builder.
htmlhelp_basename = 'REBOUNDxdoc'

# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
# The paper size ('letterpaper' or 'a4paper').
#'papersize': 'letterpaper',

# The font size ('10pt', '11pt' or '12pt').
#'pointsize': '10pt',

# Additional stuff for the LaTeX preamble.
#'preamble': '',

# Latex figure (float) alignment
#'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
  (master_doc, 'REBOUNDx.tex', 'REBOUNDx Documentation',
   'Dan Tamayo', 'manual'),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
#latex_logo = None

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
#latex_use_parts = False

# If true, show page references after internal links.
#latex_show_pagerefs = False

# If true, show URL addresses after external links.
#latex_show_urls = False

# Documents to append as an appendix to all manuals.
#latex_appendices = []

# If false, no module index is generated.
#latex_domain_indices = True


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'reboundx', 'REBOUNDx Documentation',
     [author], 1)
]

# If true, show URL addresses after external links.
#man_show_urls = False


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
  (master_doc, 'REBOUNDx', 'REBOUNDx Documentation',
   author, 'REBOUNDx', 'Library for additional physics in REBOUND simulations.',
   'Miscellaneous'),
]

# Documents to append as an appendix to all manuals.
#texinfo_appendices = []

# If false, no module index is generated.
#texinfo_domain_indices = True

# How to display URL addresses: 'footnote', 'no', or 'inline'.
#texinfo_show_urls = 'footnote'

# If true, do not generate a @detailmenu in the "Top" node's menu.
#texinfo_no_detailmenu = False


# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {'https://docs.python.org/': None}
