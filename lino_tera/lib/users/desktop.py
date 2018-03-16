# Copyright 2016 Luc Saffre
# License: BSD (see file COPYING for details)

"""Desktop UI for this plugin.

"""

from lino.modlib.users.desktop import *


class UserDetail(UserDetail):
    """Layout of User Detail in Lino Presto."""

    main = """
    box1
    remarks:40 AuthoritiesGiven:20
    """

    box1 = """
    username user_type:20 partner
    first_name last_name initials
    email language time_zone team
    id created modified
    """

Users.detail_layout = UserDetail()

