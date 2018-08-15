# -*- coding: UTF-8 -*-
# Copyright 2017-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""Defines the user types for Lino Tera.

This is used as the :attr:`user_types_module
<lino.core.site.Site.user_types_module>` for Tera sites.

"""

"""Defines a default set of user roles and fills
:class:`lino.modlib.users.choicelists.UserTypes`.

This is used as the :attr:`user_types_module
<lino.core.site.Site.user_types_module>` for
:mod:`lino_presto.projects.std`.


"""

from lino.api import _
from lino.modlib.users.choicelists import UserTypes
from lino.core.roles import UserRole, SiteAdmin, SiteUser, SiteStaff
from lino_xl.lib.contacts.roles import ContactsUser, ContactsStaff
from lino_xl.lib.products.roles import ProductsUser, ProductsStaff
from lino_xl.lib.excerpts.roles import ExcerptsUser, ExcerptsStaff
from lino_xl.lib.courses.roles import CoursesUser, CoursesTeacher
from lino_xl.lib.notes.roles import NotesUser
from lino.modlib.office.roles import OfficeStaff, OfficeUser
from lino_xl.lib.cal.roles import GuestOperator
from lino_xl.lib.ledger.roles import LedgerUser, LedgerStaff
from lino_xl.lib.sepa.roles import SepaUser, SepaStaff
from .roles import ClientsNameUser, ClientsUser


class Secretary(SiteStaff, ContactsUser, ClientsNameUser, OfficeUser,
                GuestOperator,
                LedgerStaff, SepaUser, CoursesUser, ExcerptsUser,
                ProductsStaff):
    pass


class Therapist(SiteUser, ContactsUser, ClientsUser, OfficeUser,
                # LedgerUser,
                GuestOperator, NotesUser, 
                SepaUser, CoursesTeacher, ExcerptsUser,
                ProductsUser):
    pass


class SiteAdmin(SiteAdmin, ClientsUser, ContactsStaff, OfficeStaff,
                GuestOperator, NotesUser,
                LedgerStaff, SepaStaff, CoursesUser, CoursesTeacher,
                ExcerptsStaff, ProductsStaff):
    pass

UserTypes.clear()

add = UserTypes.add_item

add('000', _("Anonymous"), UserRole, name='anonymous', readonly=True)
add('100', _("Secretary"), Secretary, name="secretary")
add('200', _("Therapist"), Therapist, name="therapist")
add('900', _("Administrator"), SiteAdmin, name='admin')

