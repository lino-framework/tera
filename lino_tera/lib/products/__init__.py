# -*- coding: UTF-8 -*-
# Copyright 2017 Luc Saffre
# License: BSD (see file COPYING for details)
"""
The :ref:`tera` extension of :mod:`lino_xl.lib.products`.

In Lino Tera we don't call them "products" but "tariffs".

And we make them less visible by moving them from the main menu to the
configuration menu.

.. autosummary::
   :toctree:

    models

"""

from lino_xl.lib.products import Plugin, _


class Plugin(Plugin):

    verbose_name = _("Tariffs")
    extends_models = ['Product', 'ProductCat']

    def setup_main_menu(self, site, user_type, m):
        pass

    def setup_config_menu(self, site, user_type, m):
        m = m.add_menu(self.app_label, self.verbose_name)
        m.add_action('products.Products')
        m.add_action('products.ProductCats')

