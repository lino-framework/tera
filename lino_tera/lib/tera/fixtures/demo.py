# -*- coding: UTF-8 -*-
# Copyright 2017 Luc Saffre
# License: BSD (see file COPYING for details)
"""Demo data for Lino Tera.

- Create a client MTI child for most persons.

"""

from django.conf import settings
from lino.utils.mti import mtichild
from lino.utils.ssin import generate_ssin
from lino.api import rt
# from lino.utils import Cycler

def objects():
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
        
