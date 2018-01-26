# -*- coding: UTF-8 -*-
# Copyright 2017 Luc Saffre
# License: BSD (see file COPYING for details)

"""The choicelists for this plugin.

"""

from lino.api import dd, _


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

