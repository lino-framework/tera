# -*- coding: UTF-8 -*-
# Copyright 2013-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from lino_xl.lib.cal.models import *


class Event(Event):

    class Meta(Event.Meta):
        abstract = dd.is_abstract_model(__name__, 'Event')
        
    def force_guest_states(self):
        if self.project and self.project.line:
            return self.project.line.course_area.force_guest_states
        return False


# The default value can remain "invited" as defined in xl because we have force_guest_states
# dd.update_field(Guest, 'state', default=GuestStates.present) # fails because GuestStates is not yet populated
# dd.update_field(Guest, 'state', default=GuestStates.as_callable('present'))
