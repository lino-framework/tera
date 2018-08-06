# -*- coding: UTF-8 -*-
# Copyright 2017-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)
"""Database models for this plugin."""

from __future__ import unicode_literals

from lino.api import _

from lino_xl.lib.contacts.models import *

#from lino_xl.lib.working.mixins import Workable

#from lino_xl.lib.coachings.mixins import Coachable
# from lino_xl.lib.courses.mixins import Enrollable

# class Partner(Partner, Coachable):

#     class Meta(Partner.Meta):
#         app_label = 'contacts'
#         abstract = dd.is_abstract_model(__name__, 'Partner')


# class Person(Person, Enrollable):

#     class Meta(Person.Meta):
#         app_label = 'contacts'
#         abstract = dd.is_abstract_model(__name__, 'Person')


# class Company(Partner, Company):

#     class Meta(Company.Meta):
#         app_label = 'contacts'
#         abstract = dd.is_abstract_model(__name__, 'Company')


dd.update_field(Person, 'first_name', blank=True)


class PartnerDetail(PartnerDetail):

    # main = 'general address more sales ledger'
    main = 'general address more ledger'

    # general = dd.Panel(PartnerDetail.main,label=_("General"))

    general = dd.Panel("""
    overview:30 ledger.MovementsByPartner #lists.MembersByPartner:20
    bottom_box
    """, label=_("General"))

    address = dd.Panel("""
    address_box contact_box
    sepa.AccountsByPartner
    """, label=_("Address"))

    # A layout for use in Belgium
    address_box = """
    prefix name id 
    addr1
    street:25 #street_no street_box
    addr2
    country zip_code:10 city
    """

    contact_box = """
    language
    email
    phone
    gsm
    fax
    """

    more = dd.Panel("""
    url
    #courses.CoursesByCompany
    # changes.ChangesByMaster
    excerpts.ExcerptsByOwner cal.GuestsByPartner
    """, label=_("More"))

    ledger_a = """
    purchase_account salesrule__invoice_recipient vat_regime
    payment_term salesrule__paper_type
    """

    # sales = dd.Panel("""
    # """, label=dd.plugins.sales.verbose_name)

    bottom_box = """
    remarks:50 checkdata.ProblemsByOwner:30
    """

    ledger = dd.Panel("""
    ledger_a 
    sales.InvoicesByPartner
    """, label=dd.plugins.ledger.verbose_name)


class CompanyDetail(CompanyDetail, PartnerDetail):

    # main = 'general more ledger'

    address = dd.Panel("""
    address_box contact_box
    contacts.RolesByCompany sepa.AccountsByPartner
    """, label=_("Address"))

    more = dd.Panel("""
    type vat_id url
    # rooms.BookingsByCompany
    notes.NotesByCompany
    """, label=_("More"))

    address_box = """
    prefix name id
    addr1
    street:25 street_no street_box
    addr2
    country zip_code:10 city
    """    

    contact_box = dd.Panel("""
    #mti_navigator
    language
    email:40
    phone
    gsm
    fax
    """)  # ,label = _("Contact"))

    bottom_box = """
    remarks:50 checkdata.ProblemsByOwner:30
    """


class PersonDetail(PersonDetail, PartnerDetail):

    main = 'general address ledger'

    general = dd.Panel("""
    overview:30  ledger.MovementsByPartner #lists.MembersByPartner:20
    bottom_box
    """, label=_("General"))

    address = dd.Panel("""
    address_box contact_box:30
    contacts.RolesByPerson sepa.AccountsByPartner
    """, label=_("Address"))

    address_box = """
    last_name first_name:15 title:10 gender
    addr1 
    street:25 street_no street_box
    addr2
    country zip_code:10 city
    """

    contact_box = """
    language
    email
    phone
    gsm
    #fax birth_date age:10
    """

    # personal = 'national_id card_number'
   
    bottom_box = """
    remarks:50 checkdata.ProblemsByOwner:30
    """
    ledger = dd.Panel("""
    id url
    sales.InvoicesByPartner
    """, label=dd.plugins.ledger.verbose_name)



# Persons.detail_layout = PersonDetail()
# Companies.detail_layout = CompanyDetail()
# Partners.detail_layout = PartnerDetail()

# Persons.set_detail_layout(PersonDetail())
# Companies.set_detail_layout(CompanyDetail())
# Partners.set_detail_layout(PartnerDetail())

from lino_xl.lib.clients.desktop import ClientContactsByCompany, ClientContactsByPerson

Company.used_as_client_contact = dd.ShowSlaveTable(ClientContactsByCompany)
Person.used_as_client_contact = dd.ShowSlaveTable(ClientContactsByPerson)
