# -*- coding: UTF-8 -*-
# Copyright 2017 Luc Saffre
# License: BSD (see file COPYING for details)
"""Database models for this plugin."""

from __future__ import unicode_literals

from lino.api import _

from lino_xl.lib.households.models import *

# from lino_xl.lib.coachings.mixins import Coachable
from lino_tera.lib.contacts.models import Partner

@dd.python_2_unicode_compatible
class Household(Household, Partner):

    class Meta(Household.Meta):
        app_label = 'households'
        abstract = dd.is_abstract_model(__name__, 'Household')

    def __str__(self):
        s = "{} {}".format(self.get_full_name(), self.type or '').strip()
        s = "{} ({})".format(s, self.pk)
        return s

class HouseholdDetail(dd.DetailLayout):

    main = "general activities"

    general = dd.Panel("""
    type prefix name id
    address_box
    bottom_box
    """, label=_("General"))

    activities = dd.Panel("""
    courses.ActivitiesByPartner
    ledger.MovementsByPartner
    """, label=_("Activities"))


    # intro_box = """
    # """

    box3 = """
    country region language:10
    city zip_code:10
    street_prefix street:25 street_no street_box
    addr2:40
    """

    box4 = """
    phone
    gsm
    email:40
    url
    """

    address_box = "box3 box4"

    bottom_box = """
    #remarks households.MembersByHousehold
    """

Households.detail_layout = HouseholdDetail()
