# -*- coding: UTF-8 -*-
# Copyright 2016 Luc Saffre
# License: BSD (see file COPYING for details)
"""Database models for this plugin."""

from __future__ import unicode_literals

from lino.api import _

from lino_xl.lib.lists.models import *


class List(List):
    
    class Meta(List.Meta):
        app_label = 'lists'
        abstract = dd.is_abstract_model(__name__, 'List')
        verbose_name = _("Therapeutical group")
        verbose_name = _("Therapeutical groups")


