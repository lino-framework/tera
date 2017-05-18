# -*- coding: UTF-8 -*-
# Copyright 2016 Luc Saffre
# License: BSD (see file COPYING for details)

"""
The `contacts` plugin specific to :ref:`psico`.

.. autosummary::
   :toctree:

    models
    fixtures
    choicelists


"""

from lino_presto.lib.contacts import Plugin


class Plugin(Plugin):

    extends_models = ['Partner', 'Person', 'Company']

