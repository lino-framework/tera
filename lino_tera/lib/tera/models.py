# -*- coding: UTF-8 -*-
# Copyright 2017 Luc Saffre
# License: BSD (see file COPYING for details)
"""Database models.

"""

from __future__ import unicode_literals
from builtins import str

from lino.api import dd, rt, _
from django.db import models
from django.conf import settings

from lino.utils import join_elems
from lino.utils.xmlgen.html import E
# from lino.utils import ssin
from lino.mixins import Referrable, CreatedModified
from lino_xl.lib.beid.mixins import BeIdCardHolder
from lino.modlib.comments.mixins import Commentable
from lino.modlib.users.mixins import UserAuthored, My

# from lino.modlib.notify.mixins import ChangeObservable
# from lino_xl.lib.notes.choicelists import SpecialTypes
from lino_xl.lib.clients.mixins import ClientBase
from lino_xl.lib.notes.mixins import Notable
from lino_tera.lib.contacts.models import Person
from lino_xl.lib.cal.workflows import TaskStates
# from lino_xl.lib.cv.mixins import BiographyOwner
# from lino.utils.mldbc.fields import BabelVirtualField

from lino.mixins import ObservedDateRange

from lino_xl.lib.clients.choicelists import ClientEvents, ClientStates

from .choicelists import StartingReasons, EndingReasons, ProfessionalStates

from .choicelists import PartnerTariffs
from lino.core.roles import Explorer
from .roles import ClientsNameUser, ClientsUser

contacts = dd.resolve_app('contacts')

# def cef_level_getter(lng):
#     def f(obj):
#         LanguageKnowledge = rt.models.cv.LanguageKnowledge
#         if obj._cef_levels is None:
#             obj._cef_levels = dict()
#             for lk in LanguageKnowledge.objects.filter(person=obj):
#                 obj._cef_levels[lk.language.iso2] = lk.obj._cef_levels
#         return obj._cef_levels.get(lng.django_code)
#     return f


@dd.python_2_unicode_compatible
class Client(Person, BeIdCardHolder, UserAuthored,
             # Referrable,
             CreatedModified,
             ClientBase,
             # Notable,
             Commentable):
    class Meta:
        app_label = 'tera'
        verbose_name = _("Patient")
        verbose_name_plural = _("Patients")
        abstract = dd.is_abstract_model(__name__, 'Client')
        #~ ordering = ['last_name','first_name']

    beid_readonly_fields = set()
    manager_roles_required = dd.login_required(ClientsUser)
    validate_national_id = True
    # workflow_state_field = 'client_state'

    # person = dd.ForeignKey("contacts.Person")

    starting_reason = StartingReasons.field(blank=True)
    ending_reason = EndingReasons.field(blank=True)
    professional_state = ProfessionalStates.field(blank=True)
    tariff = PartnerTariffs.field(
        default=PartnerTariffs.plain.as_callable())
    
    obsoletes = dd.ForeignKey(
        'self', verbose_name=_("Obsoletes"),
        blank=True, null=True, related_name='obsoleted_by')

    # translator_type = TranslatorTypes.field(blank=True)
    # translator_notes = dd.RichTextField(
    #     _("Translator"), blank=True, format='plain')
    # translator = dd.ForeignKey(
    #     "avanti.Translator",
    #     blank=True, null=True)

    

    unemployed_since = models.DateField(
        _("Unemployed since"), blank=True, null=True,
        help_text=_("Since when the client has not been employed "
                    "in any regular job."))
    seeking_since = models.DateField(
        _("Seeking work since"), blank=True, null=True,
        help_text=_("Since when the client is seeking for a job."))
    work_permit_suspended_until = models.DateField(
        blank=True, null=True, verbose_name=_("suspended until"))

    declared_name = models.BooleanField(_("Declared name"), default=False)

    # is_seeking = models.BooleanField(_("is seeking work"), default=False)
    # removed in chatelet, maybe soon also in Eupen (replaced by seeking_since)

    unavailable_until = models.DateField(
        blank=True, null=True, verbose_name=_("Unavailable until"))
    unavailable_why = models.CharField(
        _("reason"), max_length=100,
        blank=True)

    family_notes = models.TextField(
        _("Family situation"), blank=True, null=True)
    
    residence_notes = models.TextField(
        _("Residential situation"), blank=True, null=True)
    
    health_notes = models.TextField(
        _("Health situation"), blank=True, null=True)
    
    financial_notes = models.TextField(
        _("Financial situation"), blank=True, null=True)
    
    integration_notes = models.TextField(
        _("Integration notes"), blank=True, null=True)
    
    availability = models.TextField(
        _("Availability"), blank=True, null=True)

    needed_course = dd.ForeignKey(
        'courses.Line', verbose_name=_("Needed activity"),
        blank=True, null=True)
    
    # obstacles = models.TextField(
    #     _("Other obstacles"), blank=True, null=True)
    # skills = models.TextField(
    #     _("Other skills"), blank=True, null=True)

    # client_state = ClientStates.field(
    #     default=ClientStates.newcomer.as_callable)

    language_notes = dd.RichTextField(
        _("Language notes"), blank=True, format='plain')
    
    def __str__(self):
        return "%s %s (%s)" % (
            self.last_name.upper(), self.first_name, self.pk)

    def get_choices_text(self, request, actor, field):
        if request.user.user_type.has_required_roles(
                [ClientsNameUser]):
            return str(self)
        return _("{} ({}) from {}").format(
            self.first_name, self.pk, self.city)
        # return "{} {}".format(self._meta.verbose_name, self.pk)

    @dd.displayfield(_("Name"))
    def name_column(self, ar):
        return str(self)

    def get_overview_elems(self, ar):
        elems = super(Client, self).get_overview_elems(ar)
        # elems.append(E.br())
        elems.append(ar.get_data_value(self, 'eid_info'))
        # notes = []
        # for obj in rt.modules.cal.Task.objects.filter(
        #         project=self, state=TaskStates.important):
        #     notes.append(E.b(ar.obj2html(obj, obj.summary)))
        # if len(notes):
        #     notes = join_elems(notes, " / ")
        #     elems.append(E.p(*notes, class_="lino-info-yellow"))
        return elems

    # def update_owned_instance(self, owned):
    #     owned.project = self
    #     super(Client, self).update_owned_instance(owned)

    # def full_clean(self, *args, **kw):
    #     if self.national_id:
    #         ssin.ssin_validator(self.national_id)
    #     super(Client, self).full_clean(*args, **kw)

dd.update_field(Client, 'user', verbose_name=_("Primary coach"))
#dd.update_field(Client, 'ref', verbose_name=_("Legacy file number"))
    

class ClientDetail(dd.DetailLayout):

    main = "general person contact family \
    activities #notes #trends #polls misc "

    general = dd.Panel("""
    overview:30 general2:40 image:15
    cal.GuestsByPartner lists.MembersByPartner
    """, label=_("General"))

    general2 = """
    id:10 national_id:15 #ref
    birth_date age:10 gender:10
    #starting_reason professional_state
    client_state user #primary_coach
    obsoletes tariff team
    # event_policy ending_reason 
    # workflow_buttons 
    """

    contact = dd.Panel("""
    address general3
    residence_notes
    """, label=_("Residence"))

    address = """
    country city zip_code:10
    addr1
    street:25 street_no #street_box
    addr2
    """

    general3 = """
    email
    phone
    fax
    gsm
    """

    person = dd.Panel("""
    first_name middle_name last_name #declared_name
    nationality:15 birth_country birth_place 
    card_type #card_number card_issuer card_valid_from card_valid_until
    clients.ContactsByClient #uploads.UploadsByClient 
    """, label=_("Person"))

    activities = dd.Panel("""
    # courses.ActivitiesByPartner
    courses.EnrolmentsByPupil
    tera.NotesByPartner 
    # cal.GuestsByPartner
    """, label=_("Therapies"))

    family = dd.Panel("""
    family_notes:40 households.MembersByPerson:20
    #humanlinks.LinksByHuman:30
    households.SiblingsByPerson
    """, label=_("Family"))

    # notes = dd.Panel("""
    # notes.NotesByProject
    # #comments.CommentsByRFC cal.TasksByProject
    # # coachings.CoachingsByClient 
    # """, label = _("Notes"))

    # courses = dd.Panel("""
    # courses.EnrolmentsByPupil
    # """, label = _("Courses"))

    # trends = dd.Panel("""
    # trends.EventsBySubject polls.ResponsesByPartner
    # """, label = _("Trends"))

    # polls = dd.Panel("""
    # polls.ResponsesByPartner
    # """, label = _("Polls"))

    misc = dd.Panel("""
    # unavailable_until:15 unavailable_why:30
    financial_notes health_notes #integration_notes
    checkdata.ProblemsByOwner ledger.MovementsByPartner
    #excerpts.ExcerptsByProject
    """, label=_("Miscellaneous"))

    # career = dd.Panel("""
    # # unemployed_since seeking_since work_permit_suspended_until
    # cv.StudiesByPerson
    # # cv.TrainingsByPerson
    # cv.ExperiencesByPerson:40
    # """, label=_("Career"))

    # competences = dd.Panel("""
    # skills
    # obstacles
    # """, label=_("Competences"))


# Client.hide_elements('street_prefix', 'addr2')


class Clients(contacts.Persons):
    model = 'tera.Client'
    params_panel_hidden = True
    required_roles = dd.login_required(ClientsNameUser)

    # insert_layout = dd.InsertLayout("""
    # first_name last_name
    # national_id
    # gender language
    # """, window_size=(60, 'auto'))

    column_names = "name_column:20 client_state national_id:10 \
    gsm:10 address_column age:10 email phone:10 id language:10 *"

    detail_layout = ClientDetail()

    parameters = ObservedDateRange(
        nationality=dd.ForeignKey(
            'countries.Country', blank=True, null=True,
            verbose_name=_("Nationality")),
        observed_event=ClientEvents.field(blank=True),
        client_state=ClientStates.field(blank=True, default='')
    )
    params_layout = """
    #aged_from #aged_to #gender nationality client_state
    start_date end_date observed_event
    """

    @classmethod
    def get_request_queryset(self, ar):
        """This converts the values of the different parameter panel fields to
        the query filter.


        """
        qs = super(Clients, self).get_request_queryset(ar)

        pv = ar.param_values
        period = [pv.start_date, pv.end_date]
        if period[0] is None:
            period[0] = period[1] or dd.today()
        if period[1] is None:
            period[1] = period[0]

        ce = pv.observed_event
        if ce:
            qs = ce.add_filter(qs, pv)

        # if ce is None:
        #     pass
        # elif ce == ClientEvents.active:
        #     pass
        # elif ce == ClientEvents.isip:
        #     flt = has_contracts_filter('isip_contract_set_by_client', period)
        #     qs = qs.filter(flt).distinct()
        # elif ce == ClientEvents.jobs:
        #     flt = has_contracts_filter('jobs_contract_set_by_client', period)
        #     qs = qs.filter(flt).distinct()
        # elif dd.is_installed('immersion') and ce == ClientEvents.immersion:
        #     flt = has_contracts_filter(
        #         'immersion_contract_set_by_client', period)
        #     qs = qs.filter(flt).distinct()

        # elif ce == ClientEvents.available:
        #     # Build a condition "has some ISIP or some jobs.Contract
        #     # or some immersion.Contract" and then `exclude` it.
        #     flt = has_contracts_filter('isip_contract_set_by_client', period)
        #     flt |= has_contracts_filter('jobs_contract_set_by_client', period)
        #     if dd.is_installed('immersion'):
        #         flt |= has_contracts_filter(
        #             'immersion_contract_set_by_client', period)
        #     qs = qs.exclude(flt).distinct()


        if pv.client_state:
            qs = qs.filter(client_state=pv.client_state)

        if pv.nationality:
            qs = qs.filter(nationality__exact=pv.nationality)

        # print(20150305, qs.query)

        return qs

    @classmethod
    def get_title_tags(self, ar):
        for t in super(Clients, self).get_title_tags(ar):
            yield t
        pv = ar.param_values

        if pv.observed_event:
            yield unicode(pv.observed_event)

        if pv.client_state:
            yield unicode(pv.client_state)

        if pv.start_date is None or pv.end_date is None:
            period = None
        else:
            period = daterange_text(
                pv.start_date, pv.end_date)

    # @classmethod
    # def apply_cell_format(self, ar, row, col, recno, td):
    #     if row.client_state == ClientStates.newcomer:
    #         td.attrib.update(bgcolor="green")

    @classmethod
    def get_row_classes(cls, obj, ar):
        # if obj.client_state == ClientStates.newcomer:
        #     yield 'green'
        if obj.client_state in (ClientStates.refused, ClientStates.former):
            yield 'yellow'
        #~ if not obj.has_valid_card_data():
            #~ return 'red'


class AllClients(Clients):
    auto_fit_column_widths = False
    column_names = "client_state \
    starting_reason ending_reason \
    city country zip_code nationality \
    birth_date age:10 gender \
    birth_country birth_place \
    user #event_policy"
    detail_layout = None
    required_roles = dd.login_required(Explorer)



class ClientsByNationality(Clients):
    master_key = 'nationality'
    order_by = "city name".split()
    column_names = "city street street_no street_box addr2 name_column country language *"


class MyClients(My, Clients):
    pass


# class ClientsByTranslator(Clients):
#     master_key = 'translator'

from lino_xl.lib.countries.mixins import CountryCity
#from lino_xl.lib.cv.mixins import PersonHistoryEntry, HistoryByPerson

    
# class Residence(PersonHistoryEntry, CountryCity):

#     allow_cascaded_delete = ['person']

#     class Meta:
#         app_label = 'avanti'
#         verbose_name = _("Residence")
#         verbose_name_plural = _("Residences")

#     reason = models.CharField(_("Reason"), max_length=200, blank=True)



# class Residences(dd.Table):
#     model = 'avanti.Residence'
    
# class ResidencesByPerson(HistoryByPerson, Residences):
#     label = _("Former residences")
#     column_names = 'country city duration_text reason *'
#     auto_fit_column_widths = True


# @dd.receiver(dd.pre_analyze)
# def inject_cef_level_fields(sender, **kw):
#     for lng in settings.SITE.languages:
#         fld = dd.VirtualField(
#             CefLevel.field(
#                 verbose_name=lng.name, blank=True), cef_level_getter(lng))
#         dd.inject_field(
#             'avanti.Client', 'cef_level_'+lng.prefix, fld)

#     def fc(**kwargs):
#         return (**kwargs)
    

from lino.api import _, pgettext

# from lino_xl.lib.coachings.choicelists import ClientStates
# ClientStates.default_value = 'coached'
# ClientStates.clear()
# add = ClientStates.add_item
# add('10', _("Newcomer"), 'newcomer')
# # add('10', _("Testing"), 'testing')
# add('20', pgettext("client state", "Registered"), 'coached')
# add('30', _("Ended"), 'former')
# add('40', _("Abandoned"), 'refused')

# alias
# ClientStates.coached = ClientStates.newcomer


# @dd.receiver(dd.post_analyze)
# def my_details(sender, **kw):
#     sender.modules.system.SiteConfigs.set_detail_layout("""
#     site_company next_partner_id:10 default_build_method
#     # site_calendar simulate_today hide_events_before
#     # default_event_type max_auto_events 
#     """)

class NotesByPartner(dd.Table):
    # the project of a note is a course, and the partner of that
    # course is the master.
    model = 'notes.Note'
    master_key = 'project__partner'
    column_names = "date type subject project user *"
