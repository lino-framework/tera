# -*- coding: UTF-8 -*-
# Copyright 2017-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)
"""Demo data for Lino Tera.

- Create a client MTI child for most persons.

"""
from __future__ import unicode_literals

import datetime
from django.conf import settings

from lino.utils import ONE_DAY
from lino.utils.mti import mtichild
from lino.utils.ssin import generate_ssin
from lino.api import dd, rt, _
from lino.utils import Cycler
from lino.utils.mldbc import babel_named as named
from lino.modlib.users.utils import create_user

# from django.conf import settings

# courses = dd.resolve_app('courses')
# cal = dd.resolve_app('cal')
# users = dd.resolve_app('users')



def person2clients():
    Person = rt.models.contacts.Person
    Client = rt.models.tera.Client
    ClientStates = rt.models.clients.ClientStates

    count = 0
    for person in Person.objects.all():
        count += 1
        if count % 7 and person.gender and not person.birth_date:
            # most persons, but not those from humanlinks and those
            # with empty gender field, become clients. Youngest client
            # is 16; 170 days between each client
            
            birth_date = settings.SITE.demo_date(-170 * count - 16 * 365)
            national_id = generate_ssin(birth_date, person.gender)

            client = mtichild(
                person, Client, 
                national_id=national_id,
                birth_date=birth_date)

            if count % 2:
                client.client_state = ClientStates.active
            elif count % 5:
                client.client_state = ClientStates.newcomer
            else:
                client.client_state = ClientStates.closed
            yield client

        

def enrolments():
    # Person = rt.models.contacts.Person
    # Pupil = dd.plugins.courses.pupil_model
    Client = rt.models.tera.Client
    Teacher = dd.plugins.courses.teacher_model
    Line = rt.models.courses.Line
    EventType = rt.models.cal.EventType
    GuestRole = rt.models.cal.GuestRole
    Course = rt.models.courses.Course
    Line = rt.models.courses.Line
    Enrolment = rt.models.courses.Enrolment
    DurationUnits = rt.models.cal.DurationUnits
    SalesRule = rt.models.invoicing.SalesRule
    UserTypes = rt.models.users.UserTypes
    Company = rt.models.contacts.Company
    Product = rt.models.products.Product
    ProductCat = rt.models.products.ProductCat
    Account = rt.models.ledger.Account
    CommonItems = rt.models.sheets.CommonItems
    CourseAreas = rt.models.courses.CourseAreas

    yield create_user("daniel", UserTypes.therapist)
    yield create_user("elmar", UserTypes.therapist)
    yield create_user("lydia", UserTypes.secretary)

    # yield skills_objects()

    cat = ProductCat(**dd.str2kw('name', _("Payment by presence")))
    yield cat

    obj = Company(
        name="Tough Thorough Thought Therapies",
        country_id="BE", vat_id="BE12 3456 7890")
    yield obj
    settings.SITE.site_config.update(site_company=obj)

    group_therapy = named(Product, _("Group therapy"), sales_price=30, cat=cat)
    yield group_therapy
    
    indacc = named(
        Account, _("Sales on individual therapies"),
        sheet_item=CommonItems.sales.get_object(), ref="7010")
    yield indacc
    ind_therapy = named(
        Product, _("Individual therapy"),
        sales_price=60, sales_account=indacc, cat=cat)
    yield ind_therapy
    
    yield named(Product, _("Other"), sales_price=35)

    gr = GuestRole(**dd.str2kw('name', _("Attendee")))
    yield gr
    ind_et = EventType(
        force_guest_states=True,
        **dd.str2kw('name', _("Individual appointment")))
    yield ind_et
    group_et = EventType(
        force_guest_states=False,
        **dd.str2kw('name', _("Group meeting")))
    yield group_et
    
    for a in CourseAreas.get_list_items():
        kw = dict(
            name=a.text, course_area=a, guest_role=gr)
        kw.update(fees_cat=cat)
        if a.name in('therapies', 'life_groups'):
            kw.update(fee=ind_therapy, event_type=ind_et)
        else:
            kw.update(fee=group_therapy, event_type=group_et)
        a.line_obj = Line(**kw)
        yield a.line_obj  # temporary cache used below
        
    invoice_recipient = None
    for n, p in enumerate(Client.objects.all()):
        if n % 10 == 0:
            yield SalesRule(
                partner=p, invoice_recipient=invoice_recipient)
            # p.salesrule.invoice_recipient = invoice_recipient
            # yield p
        else:
            invoice_recipient = p

    # LINES = Cycler(Line.objects.all())
    USERS = Cycler(rt.models.users.User.objects.all())
    PLACES = Cycler(rt.models.cal.Room.objects.all())
    TEACHERS = Cycler(Teacher.objects.all())
    SLOTS = Cycler(rt.models.courses.Slot.objects.all())

    date = settings.SITE.demo_date(-200)
    qs = Client.objects.all()
    if qs.count() == 0:
        raise Exception("Oops, no clients!")
    PUPILS = Cycler(qs)
    kw = dict(state='draft', line=CourseAreas.therapies.line_obj)
    for i, obj in enumerate(qs):
        if i % 6:
            kw.update(
                user=USERS.pop(),
                # client=obj,
                partner=obj,
                teacher=TEACHERS.pop(),
                # line=LINES.pop(),
                room=PLACES.pop(),
                start_date=date,
                every=2,
                max_events=10,
                every_unit=DurationUnits.weeks,
                slot=SLOTS.pop())
            c = Course(**kw)
            yield c
            yield Enrolment(pupil=obj, course=c, state='confirmed')
            c.save()  # fill presences
            ar = rt.login(c.user.username)
            c.update_reminders(ar)
            date += ONE_DAY
            
    date = settings.SITE.demo_date(-200)
    kw = dict(state='draft', line=CourseAreas.default.line_obj)
    grsizes = Cycler(5, 7, 12, 6)
    group_names = (_("Alcohol"), _("Burnout"), _("Women"), _("Children"))
    for name in group_names:
        kw.update(
            user=USERS.pop(),
            # client=obj,
            name=name,
            teacher=TEACHERS.pop(),
            # line=LINES.pop(),
            room=PLACES.pop(),
            start_date=date,
            max_events=10,
            every=1,
            every_unit=DurationUnits.weeks,
            slot=SLOTS.pop())
        c = Course(**kw)
        yield c
        for i in range(grsizes.pop()):
            yield Enrolment(
                pupil=PUPILS.pop(), course=c, state='confirmed')
        c.save()  # fill presences
        ar = rt.login(c.user.username)
        c.update_reminders(ar)
        date += ONE_DAY

    # for obj in Course.objects.all():

            
def objects():
    yield person2clients()
    yield enrolments()
