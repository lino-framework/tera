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
from lino_xl.lib.accounts.utils import DEBIT
from lino_xl.lib.cal.workflows import TaskStates
from lino.utils import join_elems

from lino_xl.lib.courses.models import *

contacts = dd.resolve_app('contacts')

from lino_xl.lib.cal.utils import day_and_month

MAX_SHOWN = 3  # maximum number of invoiced events shown in
               # invoicing_info

# from lino.utils.media import TmpMediaFile

from lino.modlib.printing.utils import CustomBuildMethod


CourseAreas.clear()
add = CourseAreas.add_item
add('10', _("Individual therapies"), 'therapies', 'courses.Therapies')
add('20', _("Life groups"), 'life_groups', 'courses.LifeGroups')
add('30', _("Other groups"), 'default', 'courses.Courses')


class CourseType(Referrable, mixins.BabelNamed):

    class Meta:
        app_label = 'courses'
        abstract = dd.is_abstract_model(__name__, 'CourseType')
        verbose_name = _("Therapy type")
        verbose_name_plural = _('Therapy types')


class Line(Line):

    class Meta(Line.Meta):
        app_label = 'courses'
        abstract = dd.is_abstract_model(__name__, 'Line')

    course_type = dd.ForeignKey(
        'courses.CourseType', blank=True, null=True)


@dd.python_2_unicode_compatible
class Course(Referrable, Course):
# class Course(Course):
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

Course.set_widget_options('ref', preferred_with=6)
dd.update_field(Course, 'ref', verbose_name=_("Legacy file number"))
dd.update_field(Course, 'teacher', verbose_name=_("Therapist"))
dd.update_field(Course, 'user', verbose_name=_("Manager"))

# class CreateInvoiceForEnrolment(CreateInvoice):

#     def get_partners(self, ar):
#         return [o.pupil for o in ar.selected_rows]


class InvoicingInfo(object):
    """
    A volatile object which holds invoicing information about a given
    enrolment.

    .. attribute:: enrolment

        The enrolment it's all about.

    .. attribute:: max_date

        Don't consider dates after this.

    .. attribute:: invoiceable_fee

        Which fee to apply. If this is None, 

    .. attribute:: invoiced_qty
    """
    invoiceable_fee = None
    invoiced_qty = ZERO
    invoiced_events = 0
    used_events = []
    invoicings = None

    def __init__(self, enr, max_date=None):
        self.enrolment = enr
        self.max_date = max_date or dd.today()
        fee = enr.fee
        # fee = enr.course.fee or enr.course.line.fee
        if not fee:
            return
        if fee.min_asset is None:
            self.invoiceable_fee = fee
            return
            
        # history = []
        state_field = dd.plugins.invoicing.voucher_model._meta.get_field(
            'state')
        vstates = [s for s in state_field.choicelist.objects()
                   if not s.editable]
        # self.invoicings = enr.get_invoicings(voucher__state__in=vstates)
        self.invoicings = enr.invoicings.filter(voucher__state__in=vstates)
        if enr.free_events:
            self.invoiced_events += enr.free_events
        for obj in self.invoicings:
            if obj.product is not None:
                self.invoiced_qty += obj.qty
                if obj.product.number_of_events:
                    self.invoiced_events += int(
                        obj.qty * obj.product.number_of_events)
            # history.append("".format())
        # print("20160414", self.invoicings, self.invoiced_qty)
        start_date = enr.start_date or enr.course.start_date
        # print("20160414 a", fee.number_of_events)
        if fee.number_of_events:
            # print("20160414 b", start_date)
            if not start_date:
                return
            qs = enr.course.events_by_course.filter(
                start_date__gte=start_date,
                start_date__lte=self.max_date,
                state=rt.models.cal.EntryStates.took_place)
            if enr.end_date:
                qs = qs.filter(start_date__lte=enr.end_date)
            # Note that this query works only on the start_date of
            # events. If we want to filter on end_date, then don't
            # forget this field can be empty.
            self.used_events = qs.order_by('start_date')
            # print("20160414 c", self.used_events)
            # used_events = qs.count()
            # paid_events = invoiced_qty * fee.number_of_events
            asset = self.invoiced_events - self.used_events.count()
        else:
            asset = self.invoiced_qty
        # dd.logger.info("20160223 %s %s %s", enr, asset, fee.min_asset)
        if self.enrolment.end_date \
           and self.enrolment.end_date < self.max_date and asset >= 0:
            # ticket #1040 : a participant who declared to stop before
            # their asset got negative should not get any invoice for
            # a next asset
            return 
        if asset < fee.min_asset:
            self.invoiceable_fee = fee
            # self.invoiced_events = invoiced_events

    def as_html(self, ar):
        elems = []
        events = list(self.used_events)
        invoiced = events[self.invoiced_events:]
        coming = events[:self.invoiced_events]

        def fmt(ev):
            txt = day_and_month(ev.start_date)
            if ar is None:
                return txt
            return ar.obj2html(ev, txt)
        if len(invoiced) > 0:
            elems.append("{0} : ".format(_("Invoiced")))
            if len(invoiced) > MAX_SHOWN:
                elems.append("(...) ")
                invoiced = invoiced[-MAX_SHOWN:]
            elems += join_elems(map(fmt, invoiced), sep=', ')
            # s += ', '.join(map(fmt, invoiced))
            # elems.append(E.p(s))
        if len(coming) > 0:
            if len(elems) > 0:
                elems.append(E.br())
            elems.append("{0} : ".format(_("Not invoiced")))
            elems += join_elems(map(fmt, coming), sep=', ')
            # s += ', '.join(map(fmt, coming))
            # elems.append(E.p(s))
        return E.p(*elems)

        # for i, ev in enumerate(self.used_events):
        #     txt = day_and_month(ev.start_date)
        #     if i >= self.invoiced_events:
        #         txt = E.b(txt)
        #     elems.append(ar.obj2html(ev, txt))
        # return E.p(*join_elems(elems, sep=', '))

    def invoice_number(self, voucher):
        if self.invoicings is None:
            return 0
        n = 1
        for item in self.invoicings:
            n += 1
            if voucher and item.voucher.id == voucher.id:
                break
        return n


class Enrolment(Enrolment, Invoiceable):
    """Adds

    .. attribute:: fee

        The attendance fee to apply for this enrolment.

    .. attribute:: free_events

        Number of events to add for first invoicing for this
        enrolment.

    .. attribute:: amount

        The total amount to pay for this enrolment. This is
        :attr:`places` * :attr:`fee`.

    .. attribute:: pupil_info

        Show the name and address of the participant.  Overrides
        :attr:`lino_xl.lib.courses.models.Enrolment.pupil_info`
        in order to add (between parentheses after the name) some
        information needed to compute the price.

    .. attribute:: invoicing_info

        A virtual field showing a summary of recent invoicings.

    .. attribute:: payment_info

        A virtual field showing a summary of due accounting movements
        (debts and payments).

    """

    invoiceable_date_field = 'request_date'
    _invoicing_info = None

    class Meta:
        app_label = 'courses'
        abstract = False  # dd.is_abstract_model(__name__, 'Enrolment')
        verbose_name = _("Attendance")
        verbose_name_plural = _("Attendances")

    amount = dd.PriceField(_("Amount"), blank=True, null=True)

    fee = dd.ForeignKey('products.Product',
                        blank=True, null=True,
                        # verbose_name=_("Attendance fee"),
                        related_name='enrolments_by_fee')

    free_events = models.IntegerField(
        pgettext("in an enrolment", "Free events"),
        null=True, blank=True,
        help_text=_("Number of events to add for first invoicing "
                    "for this enrolment."))

    # create_invoice = CreateInvoiceForEnrolment()

    def get_invoiceable_partner(self):
        p = self.course.partner or self.pupil
        salesrule = getattr(p, 'salesrule', None)
        if salesrule is None:
            return p
        return salesrule.invoice_recipient or p

    def get_invoiceable_payment_term(self):
        return self.course.payment_term

    def get_invoiceable_paper_type(self):
        return self.course.paper_type

    @classmethod
    def get_invoiceables_for_plan(cls, plan, partner=None):
        """Yield all enrolments for which the given plan and partner should
        generate an invoice.

        """
        qs = cls.objects.filter(**{
            cls.invoiceable_date_field + '__lte': plan.max_date or plan.today})
        if False:  # plan.course is not None:
            qs = qs.filter(course__id=plan.course.id)
        else:
            qs = qs.filter(course__state=CourseStates.active)
        if partner is None:
            partner = plan.partner
        if partner:
            pupil = get_child(partner, rt.models.tera.Client)
            # pupil = partner.get_mti_child('pupil')
            if pupil:  # isinstance(partner, rt.models.courses.Pupil):
                q1 = models.Q(
                    pupil__salesrule__invoice_recipient__isnull=True, pupil=pupil)
                q2 = models.Q(pupil__salesrule__invoice_recipient=partner)
                qs = cls.objects.filter(models.Q(q1 | q2))
            else:
                # if the partner is not a pupil, then it might still
                # be an invoice_recipient
                qs = cls.objects.filter(pupil__salesrule__invoice_recipient=partner)
                
        # dd.logger.info("20160513 %s (%d rows)", qs.query, qs.count())
        for obj in qs.order_by(cls.invoiceable_date_field, 'id'):
            # dd.logger.info('20160223 %s', obj)
            yield obj

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
        if self.fee_id is None and self.course_id is not None:
            self.fee = self.course.fee
            if self.fee_id is None and self.course.line_id is not None:
                self.fee = self.course.line.fee
        # if self.number_of_events is None:
        #     if self.fee_id and self.fee.number_of_events:
        #         self.number_of_events = self.fee.number_of_events
        #     self.number_of_events = self.course.max_events
        if self.amount is None:
            self.compute_amount()
        super(Enrolment, self).full_clean(*args, **kwargs)

    def pupil_changed(self, ar):
        self.compute_amount()

    def places_changed(self, ar):
        self.compute_amount()

    # def fee_changed(self, ar):
    #     if self.fee_id is not None:
    #         self.number_of_events = self.fee.number_of_events
    #     self.compute_amount()

    # def get_number_of_events(self):
    #     if self.number_of_events is not None:
    #         return self.number_of_events
    #     if self.fee_id and self.fee.number_of_events:
    #         return self.fee.number_of_events
    #     return self.course.max_events or 0

    def get_invoiceable_amount(self):
        return self.amount

    def compute_amount(self):
        #~ if self.course is None:
            #~ return
        if self.places is None:
            return
        if self.fee is None:
            return
        # When `products` is not installed, then fee may be None
        # because it is a DummyField.
        price = getattr(self.fee, 'sales_price') or ZERO
        try:
            self.amount = price * self.places
        except TypeError as e:
            logger.warning("%s * %s -> %s", price, self.places, e)

    def get_invoicing_info(self, max_date=None):
        if self._invoicing_info is None:
            self._invoicing_info = InvoicingInfo(self, max_date)
        # assert self._invoicing_info.max_date == max_date
        return self._invoicing_info

    def get_invoiceable_title(self, invoice=None):
        title = _("{enrolment} to {course}").format(
            enrolment=self.__class__._meta.verbose_name,
            course=self.course)
        if self.fee.number_of_events:
            info = self.get_invoicing_info()
            number = info.invoice_number(invoice)
            if number > 1:
                msg = _("[{number}] Renewal {title}")
            else:
                msg = _("[{number}] {title}")
            return msg.format(title=title, number=number)
        return title

    def get_invoiceable_qty(self):
        return self.places

    def setup_invoice_item(self, item):
        item.description = dd.plugins.jinja.render_from_request(
            None, 'courses/Enrolment/item_description.html',
            obj=self, item=item)

    def get_invoiceable_product(self, plan):
        """Return the product to use for the invoice.
        This also decides whether an invoice should be issued or not.
        """
        # dd.logger.info('20160223 %s', self.course)
        if not self.course.state.invoiceable:
            return
        if not self.state.invoiceable:
            return
        max_date = plan.max_date or plan.today

        # the following 2 lines were nonsense. it is perfectly okay to
        # write an invoice for an enrolment which starts in the
        # future.
        # if self.start_date and self.start_date > max_date:
        #     return

        # but at least for our demo fixtures we don't want invoices
        # for enrolments in the future:
        if self.request_date and self.request_date > max_date:
            return

        return self.get_invoicing_info(max_date).invoiceable_fee

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

    @dd.displayfield(_("Invoicing info"))
    def invoicing_info(self, ar):
        info = self.get_invoicing_info(dd.today())
        return info.as_html(ar)

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

