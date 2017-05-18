# -*- coding: UTF-8 -*-
# Copyright 2016 Luc Saffre
# License: BSD (see file COPYING for details)
"""Choicelists for this plugin.

"""

from lino.api import dd, _


class PartnerTariffs(dd.ChoiceList):
    verbose_name = _("Partner tariff")
    verbose_name_plural = _("Partner tariffs")

add = PartnerTariffs.add_item

add('10', _("Plain"), 'plain')
add('20', _("Reduced"), 'reduced')


