# -*- coding: UTF-8 -*-
# Copyright 2017-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)
"""Database models for this plugin."""

from __future__ import unicode_literals

from lino.api import _

from lino_xl.lib.households.models import *

# from lino_xl.lib.coachings.mixins import Coachable
from lino_tera.lib.contacts.models import Partner
# from lino_tera.lib.courses.choicelists import PartnerTariffs
from lino_xl.lib.clients.choicelists import ClientStates

@dd.python_2_unicode_compatible
class Household(Household, Partner):

    class Meta(Household.Meta):
        app_label = 'households'
        abstract = dd.is_abstract_model(__name__, 'Household')

    # same fields as in tera.Client
    client_state = ClientStates.field(default='active')
    # tariff = PartnerTariffs.field(
    #     default=PartnerTariffs.as_callable('plain'))
    
    def __str__(self):
        s = "{} {}".format(self.get_full_name(), self.type or '').strip()
        s = "{} ({})".format(s, self.pk)
        return s

class HouseholdDetail(dd.DetailLayout):

    main = "general activities misc"

    general = dd.Panel("""
    overview address
    households.MembersByHousehold
    """, label=_("General"))

    activities = dd.Panel("""
    language:10 type salesrule__invoice_recipient client_state
    courses.ActivitiesByPartner
    """, label=_("Activities"))

    misc = dd.Panel("""
    ledger.MovementsByPartner
    """, label=_("Miscellaneous"))

    address = """
    id prefix name
    country region city zip_code:10
    addr1
    #street_prefix street:25 street_no street_box
    # addr2
    """
