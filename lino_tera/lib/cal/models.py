# -*- coding: UTF-8 -*-
# Copyright 2013-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

from __future__ import unicode_literals

from lino.api import _
from lino_xl.lib.invoicing.mixins import Invoiceable
from lino_xl.lib.cal.models import *
from lino_xl.lib.cal.choicelists import EntryStates, GuestStates
from lino_xl.lib.courses.choicelists import CourseStates
from lino_xl.lib.ledger.utils import ZERO


class Event(Event, Invoiceable):

    invoiceable_date_field = 'start_date'
    
    class Meta(Event.Meta):
        abstract = dd.is_abstract_model(__name__, 'Event')
        
    def get_invoiceable_partner(self):
        course = self.project
        p = course.partner
        if hasattr(p, 'salesrule'):
            return p.salesrule.invoice_recipient or p
        return p

    @classmethod
    def get_invoiceables_for_plan(cls, plan, partner=None):
        qs = cls.objects.filter(**{
            cls.invoiceable_date_field + '__lte':
            plan.max_date or plan.today})
        invoiceable_states = (EntryStates.took_place, EntryStates.missed)
        qs = qs.filter(project__isnull=False)
        qs = qs.filter(state__in=invoiceable_states)
        qs = qs.filter(event_type__force_guest_states=True)
        if plan.course is not None:
            qs = qs.filter(project__id=plan.course.id)
        else:
            pass
            # qs = qs.filter(event__project__state=CourseStates.active)
        if partner is None:
            partner = plan.partner
        if partner is not None:
            q1 = models.Q(
                project__partner__salesrule__invoice_recipient__isnull=True, project__partner=partner)
            q2 = models.Q(project__partner__salesrule__invoice_recipient=partner)
            qs = qs.filter(models.Q(q1 | q2))
                
        # dd.logger.info("20180923 %s (%d rows)", qs.query, qs.count())
        for obj in qs.order_by(cls.invoiceable_date_field, 'id'):
            # dd.logger.info('20160223 %s', obj)
            yield obj
            
    def get_invoiceable_product(self, plan):
        course = self.project
        if course is None:
            return
        fee = course.fee
        if fee is None and course.line_id is not None:
            fee = course.line.fee
        return fee
    
    def get_invoiceable_amount(self):
        fee = self.get_invoiceable_product(None)
        # course = self.event.project
        # fee = course.fee
        # if fee is None and course.line_id is not None:
        #     fee = course.line.fee
        return getattr(fee, 'sales_price', ZERO)
        # return self.amount

    @dd.virtualfield(dd.PriceField(_("Amount")))
    def amount(self, ar=None):
        return self.get_invoiceable_amount()

#     def force_guest_states(self):
#         if self.project and self.project.line:
#             return self.project.line.course_area.force_guest_states
#         return False


# The default value can remain "invited" as defined in xl because we have force_guest_states
# dd.update_field(Guest, 'state', default=GuestStates.present) # fails because GuestStates is not yet populated
# dd.update_field(Guest, 'state', default=GuestStates.as_callable('present'))


class Guest(Guest, Invoiceable):
    invoiceable_date_field = 'event__start_date'

    class Meta(Guest.Meta):
        abstract = dd.is_abstract_model(__name__, 'Guest')
        
    # amount = dd.PriceField(_("Amount"), blank=True, null=True)

    # fee = dd.ForeignKey('products.Product',
    #                     blank=True, null=True,
    #                     # verbose_name=_("Participation fee"),
    #                     related_name='guests_by_fee')

    def get_invoiceable_partner(self):
        p = self.partner
        if hasattr(p, 'salesrule'):
            return p.salesrule.invoice_recipient or p
        return p

    @classmethod
    def get_invoiceables_for_plan(cls, plan, partner=None):
        qs = cls.objects.filter(**{
            cls.invoiceable_date_field + '__lte':
            plan.max_date or plan.today})
        qs = qs.filter(event__project__isnull=False)
        invoiceable_states = (GuestStates.present, GuestStates.missing)
        qs = qs.filter(state__in=invoiceable_states)
        qs = qs.filter(event__event_type__force_guest_states=False)
        if plan.course is not None:
            qs = qs.filter(event__project__id=plan.course.id)
        else:
            pass
            # qs = qs.filter(event__project__state=CourseStates.active)
        if partner is None:
            partner = plan.partner
        if partner is not None:
            q1 = models.Q(
                partner__salesrule__invoice_recipient__isnull=True,
                partner=partner)
            q2 = models.Q(partner__salesrule__invoice_recipient=partner)
            qs = qs.filter(models.Q(q1 | q2))
                
        # dd.logger.info("20180923 %s (%d rows)", qs.query, qs.count())
        for obj in qs.order_by(cls.invoiceable_date_field, 'id'):
            # dd.logger.info('20160223 %s', obj)
            yield obj
            
    def get_invoiceable_product(self, plan):
        course = self.event.project
        fee = course.fee
        if fee is None and course.line_id is not None:
            fee = course.line.fee
        return fee
    
    def get_invoiceable_amount(self):
        fee = self.get_invoiceable_product(None)
        # course = self.event.project
        # fee = course.fee
        # if fee is None and course.line_id is not None:
        #     fee = course.line.fee
        return getattr(fee, 'sales_price', ZERO)
        # return self.amount

    @dd.virtualfield(dd.PriceField(_("Amount")))
    def amount(self, ar=None):
        return self.get_invoiceable_amount()

    # def full_clean(self, *args, **kwargs):
    #     if self.fee_id is None and self.event.project_id is not None:
    #         course = self.event.project
    #         self.fee = course.fee
    #         if self.fee_id is None and course.line_id is not None:
    #             self.fee = course.line.fee
    #     if self.amount is None:
    #         self.compute_amount()
    #     super(Guest, self).full_clean(*args, **kwargs)

    # def compute_amount(self):
    #     #~ if self.course is None:
    #         #~ return
    #     if self.fee is None:
    #         return
    #     # When `products` is not installed, then fee may be None
    #     # because it is a DummyField.
    #     price = getattr(self.fee, 'sales_price') or ZERO
    #     self.amount = price

Guests.detail_layout = "cal.GuestDetail"    

class GuestDetail(dd.DetailLayout):
    window_size = (60, 'auto')
    main = """
    event partner role
    state workflow_buttons 
    remark amount
    """
