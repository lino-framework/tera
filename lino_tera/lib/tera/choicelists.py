# -*- coding: UTF-8 -*-
# Copyright 2017-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""The choicelists for this plugin.

"""

from lino.api import dd, rt, _


class TranslatorTypes(dd.ChoiceList):

    """
    Types of registries for the Belgian residence.
    
    """
    verbose_name = _("Translator type")

add = TranslatorTypes.add_item
add('10', _("SETIS"))
add('20', _("Other"))
add('30', _("Private"))



class StartingReasons(dd.ChoiceList):

    verbose_name = _("Starting reason")

add = StartingReasons.add_item
add('100', _("Voluntarily"))
add('200', _("Mandatory"))

class EndingReasons(dd.ChoiceList):

    verbose_name = _("Ending reason")

add = EndingReasons.add_item
add('100', _("Successfully ended"))
add('200', _("Health problems"))
add('300', _("Familiar reasons"))
add('400', _("Missing motivation"))
add('500', _("Return to home country"))
add('900', _("Other"))


class ProfessionalStates(dd.ChoiceList):

    verbose_name = _("Professional situation")

add = ProfessionalStates.add_item
add('11', _("Independent"))
add('31', _("Employed"))
add('51', _("Student"))
add('54', _("Homemaker"))
add('61', _("Workless"))
add('63', _("Invalid"))
add('65', _("Social aid recipient"))
add('80', _("Retired"))
add('90', _("Other"))
add('00', _("Unknown"))



class PartnerTariffs(dd.ChoiceList):
    verbose_name = _("Client tariff")
    verbose_name_plural = _("Client tariffs")

add = PartnerTariffs.add_item

add('00', _("Unknown"), 'unknown')
add('10', _("Free"), 'free')
add('11', _("Tariff 2"))
add('12', _("Tariff 5"))
add('13', _("Tariff 10"))
add('14', _("Tariff 15"))
add('15', _("Tariff 20"))
add('16', _("Tariff 39,56"), 'plain')


# 01 dauert an
# 03 abgeschlossen
# 05 automatisch abgeschlossen
# 06 Abbruch der Beratung
# 09 Weitervermittlung
# 12 nur Erstkontakt


# from lino_xl.lib.clients.choicelists import ClientStates
# ClientStates.default_value = 'active'
# add = ClientStates.add_item
# add('01', _("Active"), 'active')
# add('03', _("Closed"), 'closed')
# add('05', _("Sleeping"), 'sleeping')
# add('06', _("Abandoned"), 'abandoned')
# add('09', _("Delegated"), 'delegated')  # Weitervermittlung
# add('12', _("First contact"), 'newcomer')  # Erstkontakt

from lino_xl.lib.clients.choicelists import ClientStates
ClientStates.default_value = None
ClientStates.clear()
add = ClientStates.add_item
# add('01', pgettext("client state", "Active"), 'active')
add('01', _("Active"), 'active')
add('03', _("Closed"), 'closed')
add('05', _("Cancelled"), 'cancelled')  # auto_closed')
add('06', _("Abandoned"), 'abandoned')
add('09', _("Forwarded"), 'forwarded')
add('12', _("Newcomer"), 'newcomer')
# obsolete values still used on old data
add('00', _("00"))
add('02', _("02"))
add('04', _("04"))
add('08', _("08"))
add('10', _("10"))
add('11', _("11"))
add('99', _("99"))

CT = ClientStates.active.add_transition(required_states="cancelled abandoned newcomer")
CT = ClientStates.closed.add_transition(required_states="cancelled active abandoned forwarded newcomer")
CT = ClientStates.forwarded.add_transition(required_states="active newcomer")

from lino_xl.lib.courses.choicelists import EnrolmentStates
EnrolmentStates.default_value = 'confirmed'
EnrolmentStates.clear()
add = EnrolmentStates.add_item
add('01', _("Confirmed"), 'confirmed', invoiceable=True, uses_a_place=True)
add('03', _("Closed"), 'closed', invoiceable=False, uses_a_place=False)
add('05', _("Cancelled"), 'cancelled', invoiceable=False, uses_a_place=False)
add('06', _("Abandoned"), 'abandoned', invoiceable=False, uses_a_place=False)
add('09', _("Forwarded"), 'forwarded', invoiceable=False, uses_a_place=False)
add('12', _("Requested"), 'requested', invoiceable=False, uses_a_place=False)
add('00', _("Trying"), 'trying', invoiceable=False, uses_a_place=False)
add('02', _("Active"), 'active', invoiceable=True, uses_a_place=True)
add('04', _("04"), invoiceable=False, uses_a_place=False)
add('08', _("08"), invoiceable=False, uses_a_place=False)
add('11', _("11"), invoiceable=False, uses_a_place=False)
add('99', _("99"), invoiceable=False, uses_a_place=False)


from lino_xl.lib.cal.workflows import EntryStates
add = EntryStates.add_item
add('60', _("Missed"), 'missed', fixed=True)

