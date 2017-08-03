# -*- coding: UTF-8 -*-
# Copyright 2017 Luc Saffre
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
from lino.api import dd, rt
from lino.utils import Cycler

# from django.conf import settings

# courses = dd.resolve_app('courses')
# cal = dd.resolve_app('cal')
# users = dd.resolve_app('users')




def person2clients():
    Person = rt.models.contacts.Person
    Client = rt.models.tera.Client
    ClientStates = rt.actors.coachings.ClientStates

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
                client.client_state = ClientStates.coached
            # elif count % 5:
            #     client.client_state = ClientStates.newcomer
            else:
                client.client_state = ClientStates.former
            yield client

        

def enrolments():
    # Person = rt.models.contacts.Person
    # Pupil = dd.plugins.courses.pupil_model
    Client = rt.models.tera.Client
    Teacher = dd.plugins.courses.teacher_model
    Line = rt.models.courses.Line
    Course = rt.models.courses.Course
    Enrolment = rt.models.courses.Enrolment
    DurationUnits = rt.models.cal.DurationUnits

    for a in rt.models.courses.CourseAreas.get_list_items():
        yield Line(name=a.text, course_area=a)
        
    invoice_recipient = None
    for n, p in enumerate(Client.objects.all()):
        if n % 10 == 0:
            p.invoice_recipient = invoice_recipient
            yield p
        else:
            invoice_recipient = p

    LINES = Cycler(Line.objects.all())
    USERS = Cycler(rt.models.users.User.objects.all())
    PLACES = Cycler(rt.models.cal.Room.objects.all())
    TEACHERS = Cycler(Teacher.objects.all())
    SLOTS = Cycler(rt.models.courses.Slot.objects.all())

    date = settings.SITE.demo_date(-200)
    qs = Client.objects.all()
    if qs.count() == 0:
        raise Exception("Oops, no clients!")
    for i, obj in enumerate(qs):
        if True:
            c = Course(
                user=USERS.pop(),
                # client=obj,
                partner=obj,
                teacher=TEACHERS.pop(),
                line=LINES.pop(), room=PLACES.pop(),
                start_date=date,
                every=1,
                every_unit=DurationUnits.weeks,
                slot=SLOTS.pop(),
            )
            yield c
            yield Enrolment(pupil=obj, course=c)

            c.save()  # fill presences

            date += ONE_DAY

            
def objects():
    yield person2clients()
    yield enrolments()
