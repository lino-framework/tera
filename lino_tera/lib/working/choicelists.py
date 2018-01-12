# -*- coding: UTF-8 -*-
# Copyright 2016 Luc Saffre
# License: BSD (see file COPYING for details)
"""Choicelists for :mod:`lino_presto.lib.working`.

"""

from __future__ import unicode_literals

from django.db import models
from lino.api import dd, _


class PaymentModes(dd.ChoiceList):
    verbose_name = _("Payment mode")
    verbose_name_plural = _("Payment modes")

add = PaymentModes.add_item

add('10', _("Free"), 'free')
add('20', _("Cash"), 'cash')
add('30', _("Invoice"), 'invoice')
add('40', _("Later"), 'later')


class SessionStates(dd.Workflow):
    required_roles = dd.login_required(dd.SiteAdmin)
    invoiceable = models.BooleanField(_("invoiceable"), default=True)

add = SessionStates.add_item
add('10', _("Draft"), 'draft', editable=True, invoiceable=False)
add('20', _("Closed"), 'closed', editable=False, invoiceable=False)
add('30', _("Cancelled"), 'cancelled', editable=False, invoiceable=False)
add('40', _("Missed"), 'missed', editable=False, invoiceable=True)

