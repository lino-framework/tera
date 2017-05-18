# -*- coding: UTF-8 -*-
# Copyright 2016 Luc Saffre
# License: BSD (see file COPYING for details)

"""
The `clocking` plugins specific to :ref:`psico`.

.. autosummary::
   :toctree:

    models
    fixtures
    choicelists


"""

from lino_xl.lib.clocking import Plugin


class Plugin(Plugin):

    extends_models = ['Session']

    ticket_model = 'contacts.Partner'
