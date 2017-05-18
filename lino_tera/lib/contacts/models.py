# -*- coding: UTF-8 -*-
# Copyright 2016 Luc Saffre
# License: BSD (see file COPYING for details)
"""Database models for this plugin."""

from __future__ import unicode_literals

from lino.api import _

from lino_presto.lib.contacts.models import *

from .choicelists import PartnerTariffs
from lino_xl.lib.clocking.mixins import Workable


class Partner(Partner, Workable):

    class Meta(Partner.Meta):
        app_label = 'contacts'
        abstract = dd.is_abstract_model(__name__, 'Partner')

    obsoletes = dd.ForeignKey(
        'self', blank=True, null=True, related_name='obsoleted_by')

    tariff = PartnerTariffs.field(
        default=PartnerTariffs.plain.as_callable())


class Person(Partner, Person):

    class Meta(Person.Meta):
        app_label = 'contacts'
        abstract = dd.is_abstract_model(__name__, 'Person')


class Company(Partner, Company):

    class Meta(Company.Meta):
        app_label = 'contacts'
        abstract = dd.is_abstract_model(__name__, 'Company')


dd.update_field(Person, 'first_name', blank=True)
