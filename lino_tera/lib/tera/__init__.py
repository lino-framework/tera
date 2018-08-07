# -*- coding: UTF-8 -*-
# Copyright 2014-2017 Luc Saffre
# License: BSD (see file COPYING for details)
"""
The main plugin for Lino Tera.

.. autosummary::
   :toctree:

    models
    migrate
    user_types
    workflows
    layouts

"""

from lino.api.ad import Plugin


class Plugin(Plugin):

    def setup_main_menu(self, site, user_type, m):
        mg = site.plugins.contacts
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('tera.Clients')
