# -*- coding: UTF-8 -*-
# Copyright 2016-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)
"""
The default :attr:`workflows_module
<lino.core.site.Site.workflows_module>` for :ref:`tera` applications.

This workflow requires that both :mod:`lino_xl.lib.cal` and
:mod:`lino_xl.lib.courses` are installed.

"""
from __future__ import unicode_literals

#from lino_noi.lib.tickets.workflows import *
from lino_xl.lib.cal.workflows.voga import *
from lino_xl.lib.courses.workflows import *
from lino.api import _

from lino_xl.lib.cal.choicelists import EntryStates, GuestStates

# EntryStates.override_transition(
#     "cancel",
#     required_states='missed suggested draft took_place')
EntryStates.missed.add_transition(
    required_states='cancelled suggested draft took_place')

EntryStates.took_place.guest_state = GuestStates.present
EntryStates.cancelled.guest_state = GuestStates.excused
EntryStates.missed.guest_state = GuestStates.missing
