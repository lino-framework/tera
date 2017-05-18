# -*- coding: UTF-8 -*-
# Copyright 2016 Luc Saffre
# License: BSD (see file COPYING for details)
"""The `demo` fixture for this plugin."""

from lino.api import rt, dd, _


def objects():
    List = rt.models.lists.List
    for y in (2014, 2015, 2016):
        yield List(**dd.str2kw('name', _("Women's group {0}").format(y)))
        yield List(**dd.str2kw('name', _("Men's group {0}").format(y)))
        yield List(**dd.str2kw('name', _("Children's group {0}").format(y)))

