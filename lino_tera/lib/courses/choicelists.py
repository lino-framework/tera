# -*- coding: UTF-8 -*-
# Copyright 2017-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

from lino.api import dd, rt, _

from lino_xl.lib.courses.choicelists import *

CourseAreas.clear()
add = CourseAreas.add_item
add('IT', _("Individual therapies"), 'therapies', 'courses.Therapies')
    # force_guest_states=True)
add('LG', _("Life groups"), 'life_groups', 'courses.LifeGroups')
    # force_guest_states=True)
add('OG', _("Other groups"), 'default', 'courses.Courses')


# Stand der Beratung:
# 01 dauert an                                
# 03 abgeschlossen                            
# 05 automatisch abgeschlossen                
# 06 Abbruch der Beratung                     
# 09 Weitervermittlung                        
# 12 nur Erstkontakt
CourseStates.clear()
add = CourseStates.add_item
add('01', _("Active"), 'active',
    is_editable=True, is_invoiceable=True, is_exposed=True,
    auto_update_calendar=False)
add('03', _("Closed"), 'closed',
    is_editable=False, is_invoiceable=False, is_exposed=False,
    auto_update_calendar=False)
add('05', _("Inactive"), 'inactive',
    is_editable=False, is_invoiceable=False, is_exposed=False,
    auto_update_calendar=False)
add('06', _("Cancelled"), 'cancelled',
    is_editable=False, is_invoiceable=False, is_exposed=False,
    auto_update_calendar=False)
add('09', _("Forwarded"), 'forwarded',
    is_editable=False, is_invoiceable=False, is_exposed=False,
    auto_update_calendar=False)
add('12', _("Draft"), 'draft',
    is_editable=True, is_invoiceable=False, is_exposed=True,
    auto_update_calendar=False)

# EnrolmentStates.default_value = 'confirmed'
EnrolmentStates.clear()
add = EnrolmentStates.add_item
add('01', _("Confirmed"), 'confirmed', invoiceable=True, uses_a_place=True)
add('03', _("Closed"), 'closed', invoiceable=False, uses_a_place=False)
add('05', _("Inactive"), 'inactive', invoiceable=False, uses_a_place=False)
add('06', _("Cancelled"), 'cancelled', invoiceable=False, uses_a_place=False)
add('09', _("Forwarded"), 'forwarded', invoiceable=False, uses_a_place=False)
add('12', _("First contact"), 'requested', invoiceable=False, uses_a_place=False)
add('00', _("Trying"), 'trying', invoiceable=False, uses_a_place=False)
add('02', _("Active"), 'active', invoiceable=True, uses_a_place=True)
# add('04', _("04"), invoiceable=False, uses_a_place=False)
# add('08', _("08"), invoiceable=False, uses_a_place=False)
# add('11', _("11"), invoiceable=False, uses_a_place=False)
# add('99', _("99"), invoiceable=False, uses_a_place=False)


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

