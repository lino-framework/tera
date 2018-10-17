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

from lino_xl.lib.courses.models import *

contacts = dd.resolve_app('contacts')

from lino_xl.lib.cal.utils import day_and_month

# from lino.utils.media import TmpMediaFile

from lino.modlib.printing.utils import CustomBuildMethod


CourseAreas.clear()
add = CourseAreas.add_item
add('10', _("Individual therapies"), 'therapies', 'courses.Therapies')
    # force_guest_states=True)
add('20', _("Life groups"), 'life_groups', 'courses.LifeGroups')
    # force_guest_states=True)
add('30', _("Other groups"), 'default', 'courses.Courses')


# class CourseType(Referrable, mixins.BabelNamed):

#     class Meta:
#         app_label = 'courses'
#         abstract = dd.is_abstract_model(__name__, 'CourseType')
#         verbose_name = _("Therapy type")
#         verbose_name_plural = _('Therapy types')


class Line(Line):

    class Meta(Line.Meta):
        app_label = 'courses'
        abstract = dd.is_abstract_model(__name__, 'Line')
        verbose_name = _("Therapy type")
        verbose_name_plural = _('Therapy types')

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

    partner = dd.ForeignKey(
        'contacts.Partner',
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
        if self.name:
            if self.ref:
                s = "{0} {1}".format(self.ref, self.name)
            else:
                s = self.name
        elif self.ref:
            if self.line:
                s = "{0} {1}".format(self.ref, self.line)
            else:
                s = self.ref
        else:
            # Note that we cannot use super() with
            # python_2_unicode_compatible
            s = "{0} #{1}".format(self._meta.verbose_name, self.pk)
        if self.teacher:
            s = "{} ({})".format(
                s, self.teacher.initials or self.teacher)
        return s

    def update_cal_summary(self, et, i):
        label = dd.babelattr(et, 'event_label')
        if self.ref:
            label = self.ref + ' ' + label
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

# Course.set_widget_options('ref', preferred_with=6)
# dd.update_field(Course, 'ref', verbose_name=_("Legacy file number"))
dd.update_field(Course, 'teacher', verbose_name=_("Therapist"))
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

    class Meta:
        app_label = 'courses'
        abstract = False  # dd.is_abstract_model(__name__, 'Enrolment')
        verbose_name = _("Attendance")
        verbose_name_plural = _("Attendances")

    fee = dd.ForeignKey('products.Product',
                        blank=True, null=True,
                        # verbose_name=_("Attendance fee"),
                        related_name='enrolments_by_fee')

    # free_events = models.IntegerField(
    #     pgettext("in an enrolment", "Free events"),
    #     null=True, blank=True,
    #     help_text=_("Number of events to add for first invoicing "
    #                 "for this enrolment."))

    # create_invoice = CreateInvoiceForEnrolment()

    # def get_invoiceable_partner(self):
    #     p = self.course.partner or self.pupil
    #     salesrule = getattr(p, 'salesrule', None)
    #     if salesrule is None:
    #         return p
    #     return salesrule.invoice_recipient or p

    # def get_invoiceable_payment_term(self):
    #     return self.course.payment_term

    # def get_invoiceable_paper_type(self):
    #     return self.course.paper_type

    # @classmethod
    # def get_invoiceables_for_plan(cls, plan, partner=None):
    #     """Yield all enrolments for which the given plan and partner should
    #     generate an invoice.

    #     """
    #     qs = cls.objects.filter(**{
    #         cls.invoiceable_date_field + '__lte': plan.max_date or plan.today})
    #     if False:  # plan.course is not None:
    #         qs = qs.filter(course__id=plan.course.id)
    #     else:
    #         qs = qs.filter(course__state=CourseStates.active)
    #     if partner is None:
    #         partner = plan.partner
    #     if partner:
    #         pupil = get_child(partner, rt.models.tera.Client)
    #         # pupil = partner.get_mti_child('pupil')
    #         if pupil:  # isinstance(partner, rt.models.courses.Pupil):
    #             q1 = models.Q(
    #                 pupil__salesrule__invoice_recipient__isnull=True, pupil=pupil)
    #             q2 = models.Q(pupil__salesrule__invoice_recipient=partner)
    #             qs = cls.objects.filter(models.Q(q1 | q2))
    #         else:
    #             # if the partner is not a pupil, then it might still
    #             # be an invoice_recipient
    #             qs = cls.objects.filter(pupil__salesrule__invoice_recipient=partner)
                
    #     # dd.logger.info("20160513 %s (%d rows)", qs.query, qs.count())
    #     for obj in qs.order_by(cls.invoiceable_date_field, 'id'):
    #         # dd.logger.info('20160223 %s', obj)
    #         yield obj

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
        

# dd.inject_field(
#     'products.Product', 'number_of_events',
#     models.IntegerField(
#         _("Number of events"), null=True, blank=True,
#         help_text=_("Number of events paid per invoicing.")))

# dd.inject_field(
#     'products.Product', 'min_asset',
#     models.IntegerField(
#         _("Invoice threshold"), null=True, blank=True,
#         help_text=_("Minimum number of events to pay in advance.")))

