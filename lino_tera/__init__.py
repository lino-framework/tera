# -*- coding: UTF-8 -*-
# Copyright 2014-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)
"""This is the main module of Lino Tera.

.. autosummary::
   :toctree:

   lib


"""

from .setup_info import SETUP_INFO

__version__ = SETUP_INFO['version']

intersphinx_urls = dict(docs="http://tera.lino-framework.org")
srcref_url = 'https://github.com/lino-framework/tera/blob/master/%s'
doc_trees = ['docs']

