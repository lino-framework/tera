# -*- coding: UTF-8 -*-
# Copyright 2017-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

from lino.api import dd, rt, _

class TranslatorTypes(dd.ChoiceList):
    verbose_name = _("Translator type")
    verbose_name_plural = _("Translator types")

add = TranslatorTypes.add_item
add('10', _("Interpreter"), "interpreter")
add('20', _("SETIS"))
add('30', _("Other"))


class TherapyDomains(dd.ChoiceList):
    verbose_name = _("Therapy domain")
    verbose_name_plural = _("Therapy domain")

add = TherapyDomains.add_item
add('E', _("Adults"), "adults")
add('M', _("Children M"))
add('P', _("Children P"))



class EndingReasons(dd.ChoiceList):

    verbose_name = _("Ending reason")

add = EndingReasons.add_item
add('100', _("Successfully ended"))
add('200', _("Health problems"))
add('300', _("Familiar reasons"))
add('400', _("Missing motivation"))
add('500', _("Return to home country"))
add('900', _("Other"))


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

