# -*- coding: UTF-8 -*-
# Copyright 2017 Luc Saffre
# License: BSD (see file COPYING for details)
"""Database models for this plugin."""

from __future__ import unicode_literals

from lino.api import _

from lino_xl.lib.contacts.models import *

#from lino_xl.lib.clocking.mixins import Workable

from lino_xl.lib.coachings.mixins import Coachable

class Partner(Partner, Coachable):

    class Meta(Partner.Meta):
        app_label = 'contacts'
        abstract = dd.is_abstract_model(__name__, 'Partner')


class Person(Partner, Person):

    class Meta(Person.Meta):
        app_label = 'contacts'
        abstract = dd.is_abstract_model(__name__, 'Person')


class Company(Partner, Company):

    class Meta(Company.Meta):
        app_label = 'contacts'
        abstract = dd.is_abstract_model(__name__, 'Company')


dd.update_field(Person, 'first_name', blank=True)
