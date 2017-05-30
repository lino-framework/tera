# -*- coding: UTF-8 -*-
# Copyright 2016-2017 Luc Saffre
# License: BSD (see file COPYING for details)
"""Database models for this plugin."""

from __future__ import unicode_literals

from lino.api import _

from lino_xl.lib.lists.models import *
# from lino_xl.lib.coachings.mixins import Coachable
from lino_tera.lib.contacts.models import Partner


class List(List, Partner):
    
    class Meta(List.Meta):
        app_label = 'lists'
        abstract = dd.is_abstract_model(__name__, 'List')
        verbose_name = _("Therapeutical group")
        verbose_name = _("Therapeutical groups")


