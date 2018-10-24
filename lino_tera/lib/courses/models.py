# -*- coding: UTF-8 -*-
# Copyright 2013-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""
Database models for this plugin.

.. xfile:: courses/Enrolment/item_description.html

     The template used to fill the items description.

"""

from __future__ import unicode_literals
from __future__ import print_function

from builtins import str

from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy as pgettext
from django.db import models

from lino.utils.mti import get_child
from lino.api import dd, rt
from etgen.html import E

from lino.mixins import Referrable
from lino.modlib.printing.mixins import Printable
from lino_xl.lib.invoicing.mixins import Invoiceable
from lino_xl.lib.courses.mixins import Enrollable
from lino_xl.lib.ledger.utils import DEBIT
from lino_xl.lib.cal.workflows import TaskStates
from lino.utils import join_elems

from .choicelists import EndingReasons, TranslatorTypes
from .choicelists import PartnerTariffs, TherapyDomains

from lino_xl.lib.courses.models import *
from .choicelists import *

contacts = dd.resolve_app('contacts')

from lino_xl.lib.cal.utils import day_and_month

# from lino.utils.media import TmpMediaFile

from lino.modlib.printing.utils import CustomBuildMethod



class Line(Line):

    class Meta(Line.Meta):
        app_label = 'courses'
        abstract = dd.is_abstract_model(__name__, 'Line')
        verbose_name = _("Therapy type")
        verbose_name_plural = _('Therapy types')

    ref_max_length = 4

    # course_type = dd.ForeignKey(
    #     'courses.CourseType', blank=True, null=True)


@dd.python_2_unicode_compatible
class Course(Referrable, Course):
    """Extends the standard model by adding a field :attr:`fee`.

    Also adds a :attr:`ref` field and defines a custom :meth:`__str__`
    method.

    The custom :meth:`__str__` method defines how to textually
    represent a course e.g. in the dropdown list of a combobox or in
    reports. Rules:

    - If :attr:`ref` is given, it is shown, but see also the two
      following cases.

    - If :attr:`name` is given, it is shown (possibly behind the
      :attr:`ref`).

    - If a :attr:`line` (series) is given, it is shown (possibly
      behind the :attr:`ref`).

    - If neither :attr:`ref` nor :attr:`name` nor :attr:`line` are
      given, show a simple "Course #".


    .. attribute:: ref
    
        An identifying public course number to be used by both
        external and internal partners for easily referring to a given
        course.

    .. attribute:: name

        A short designation for this course. An extension of the
        :attr:`ref`.

    .. attribute:: line

        Pointer to the course series.


    .. attribute:: fee

        The default attendance fee to apply for new enrolments.

    .. attribute:: payment_term

        The payment term to use when writing an invoice. If this is
        empty, Lino will use the partner's default payment term.

    .. attribute:: paper_type

        The paper_type to use when writing an invoice. If this is
        empty, Lino will use the site's default paper type.

    """
    class Meta(Course.Meta):
        app_label = 'courses'
        abstract = dd.is_abstract_model(__name__, 'Course')
        verbose_name = _("Therapy")
        verbose_name_plural = _('Therapies')

    ref_max_length = 8
    
    # allow_cascaded_delete = "client household"
    allow_cascaded_delete = "partner"

    fee = dd.ForeignKey('products.Product',
                        blank=True, null=True,
                        verbose_name=_("Default attendance fee"),
                        related_name='courses_by_fee')

    payment_term = dd.ForeignKey(
        'ledger.PaymentTerm',
        related_name="%(app_label)s_%(class)s_set_by_payment_term",
        blank=True, null=True)    

    procurer = dd.ForeignKey('tera.Procurer', blank=True, null=True)
    mandatory = models.BooleanField(_("Mandatory"), default=False)
    ending_reason = EndingReasons.field(blank=True)
    tariff = PartnerTariffs.field(
        default=PartnerTariffs.as_callable('plain'))
    translator_type = TranslatorTypes.field(blank=True)
    therapy_domain = TherapyDomains.field(blank=True)
    team = dd.ForeignKey('teams.Team', blank=True, null=True)
    
    partner = dd.ForeignKey(
        'contacts.Partner',
        verbose_name=_("Invoice recipient"),
        # related_name="%(app_label)s_%(class)s_set_by_client",
        blank=True, null=True)    

    # client = dd.ForeignKey(
    #     'tera.Client',
    #     related_name="%(app_label)s_%(class)s_set_by_client",
    #     blank=True, null=True)    

    # household = dd.ForeignKey(
    #     'households.Household',
    #     related_name="%(app_label)s_%(class)s_set_by_household",
    #     blank=True, null=True)    

    paper_type = dd.ForeignKey(
        'sales.PaperType',
        related_name="%(app_label)s_%(class)s_set_by_paper_type",
        blank=True, null=True)    

    quick_search_fields = 'name line__name line__topic__name ref'

    @classmethod
    def get_registrable_fields(cls, site):
        for f in super(Course, cls).get_registrable_fields(site):
            yield f
        yield 'fee'

    @dd.chooser()
    def fee_choices(cls, line):
        Product = rt.models.products.Product
        if not line or not line.fees_cat:
            return Product.objects.none()
        return Product.objects.filter(cat=line.fees_cat)

    def full_clean(self):
        if not self.name:
            # self.name = str(self.household or self.client)
            # if self.partner.team and self.partner.team.ref:
            #     s = self.partner.team.ref + "/"
            # else:
            #     s = ''
            if self.partner:
                s = self.partner.name
            else:
                s = 'ZZZ'
            if self.line_id and self.line.ref:
                s = "{} ({})".format(s, self.line.ref)
            self.name = s
        return super(Course, self).full_clean()
    
    def __str__(self):
        if self.line and self.line.ref:
            s = self.line.ref + ' '
        else:
            s = ''
        if self.ref:
            s += " " + self.ref
        if self.name:
            s += ' ' + self.name
        else:
            # Note that we cannot use super() with
            # python_2_unicode_compatible
            s += "{0} #{1}".format(self._meta.verbose_name, self.pk)
        if self.teacher and self.teacher.initials:
            s = "{} ({})".format(s, self.teacher.initials)
        return s

    def update_cal_summary(self, et, i):
        label = dd.babelattr(et, 'event_label')
        if self.ref:
            label = self.ref + ' ' + label
        if self.line and self.line.ref:
            label = self.line.ref + '.' + label
        return "%s %d" % (label, i)

    def get_overview_elems(self, ar):
        # we don't want to see the teacher (therapist)
        # here. Especially not in MyGivenCourses but probably nowhere
        # else either.  when a table of therapies is shown in
        # dashboard, then we want a way to open its detail with a
        # single click.
        
        # elems = super(Course, self).get_overview_elems(ar)
        elems = []
        elems.append(self.obj2href(ar))
        # if self.teacher_id:
        #     elems.append(" / ")
        #     # elems.append(ar.obj2html(self.teacher))
        #     elems.append(self.teacher.obj2href(ar))
        # elems.append(E.br())
        # elems.append(ar.get_data_value(self, 'eid_info'))
        notes = []
        for obj in rt.models.cal.Task.objects.filter(
                project=self, state=TaskStates.important):
            notes.append(E.b(ar.obj2html(obj, obj.summary)))
        if len(notes):
            notes = join_elems(notes, " / ")
            elems.append(E.p(*notes, **{'class':"lino-info-yellow"}))
        return elems

    def update_owned_instance(self, owned):
        owned.project = self
        super(Course, self).update_owned_instance(owned)

    @dd.displayfield(_("Patient"))
    def client(self, ar):
        if ar is None or self.partner_id is None:
            return
        obj = get_child(self.partner, rt.models.tera.Client)
        if obj is not None:
            return obj.obj2href(ar)

    @dd.displayfield(_("Household"))
    def household(self, ar):
        if ar is None or self.partner_id is None:
            return
        obj = get_child(self.partner, rt.models.households.Household)
        if obj is not None:
            return obj.obj2href(ar)

    @dd.displayfield(_("Organization"))
    def company(self, ar):
        if ar is None or self.partner_id is None:
            return
        obj = get_child(self.partner, rt.models.contacts.Company)
        if obj is not None:
            return obj.obj2href(ar)

# Course.set_widget_options('ref', preferred_with=6)
# dd.update_field(Course, 'ref', verbose_name=_("Legacy file number"))
# dd.update_field(Course, 'partner', verbose_name=_("Invoicing address"))
#  dd.update_field(Course, 'teacher', verbose_name=_("Therapist"))
dd.update_field(Course, 'user', verbose_name=_("Manager"))

# class CreateInvoiceForEnrolment(CreateInvoice):

#     def get_partners(self, ar):
#         return [o.pupil for o in ar.selected_rows]


class Enrolment(Enrolment):
    """Adds

    .. attribute:: fee

        The fee per appointment to apply for this enrolment.

    .. attribute:: pupil_info

        Show the name and address of the participant.  Overrides
        :attr:`lino_xl.lib.courses.models.Enrolment.pupil_info`
        in order to add (between parentheses after the name) some
        information needed to compute the price.

    .. attribute:: payment_info

        A virtual field showing a summary of due accounting movements
        (debts and payments).

    """

    class Meta(Enrolment.Meta):
        app_label = 'courses'
        abstract = dd.is_abstract_model(__name__, 'Enrolment')
        # verbose_name = _("Attendance")
        # verbose_name_plural = _("Attendances")

    guest_role = dd.ForeignKey(
        'cal.GuestRole', verbose_name=_("Role"), blank=True, null=True)
    fee = dd.ForeignKey('products.Product',
                        blank=True, null=True,
                        # verbose_name=_("Attendance fee"),
                        related_name='enrolments_by_fee')

    @dd.chooser()
    def fee_choices(cls, course):
        Product = rt.models.products.Product
        if not course or not course.line or not course.line.fees_cat:
            return Product.objects.none()
        return Product.objects.filter(cat=course.line.fees_cat)

    def full_clean(self, *args, **kwargs):
        # if self.state == EnrolmentStates.requested:
        #     self.state = EnrolmentStates.get_by_value(
        #         self.pupil.client_state.value) or EnrolmentStates.requested
        if self.guest_role_id is None:
            if self.course.line_id:
                self.guest_roles = self.course.line.guest_role
        if self.fee_id is None:
            self.compute_fee()
        super(Enrolment, self).full_clean(*args, **kwargs)

    def pupil_changed(self, ar):
        self.compute_fee()

    def compute_fee(self):
        #todo: set fee according to tariff rules
        if self.course_id is not None:
            self.fee = self.course.fee
            if self.fee_id is None and self.course.line_id is not None:
                self.fee = self.course.line.fee

    @dd.virtualfield(dd.HtmlBox(_("Participant")))
    def pupil_info(self, ar):
        if not self.pupil_id:
            return ''
        elems = []
        txt = self.pupil.get_full_name(nominative=True)
        if ar is None:
            elems = [txt]
        else:
            elems = [ar.obj2html(self.pupil, txt)]
        info = self.pupil.get_enrolment_info()
        if info:
            # elems += [" ({})".format(self.pupil.pupil_type.ref)]
            elems += [" ({})".format(info)]
        elems += [', ']
        elems += join_elems(
            self.pupil.address_location_lines(), sep=', ')
        if self.pupil.phone:
            elems += [', ', _("Phone: {0}").format(self.pupil.phone)]
        if self.pupil.gsm:
            elems += [', ', _("GSM: {0}").format(self.pupil.gsm)]
        return E.p(*elems)

    @dd.displayfield(_("Payment info"))
    def payment_info(self, ar):
        if not self.pupil_id:
            return ''
        return rt.models.ledger.Movement.balance_info(
            DEBIT, partner=self.pupil, cleared=False)
        
    def get_guest_role(self):
        return self.guest_role or super(Enrolment, self).get_guest_role()
        

dd.update_field(
    Enrolment, 'overview',
    verbose_name=Course._meta.verbose_name)
