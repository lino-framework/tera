# -*- coding: UTF-8 -*-
# Copyright 2016 Luc Saffre
# License: BSD (see file COPYING for details)
"""The `demo` fixture for this plugin."""

from lino.api import rt, _


def objects():
    Team = rt.models.teams.Team
    yield Team(name="Eupen")
    yield Team(name="St.Vith")

