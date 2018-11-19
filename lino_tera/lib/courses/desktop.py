# -*- coding: UTF-8 -*-
# Copyright 2013-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

# 

from __future__ import unicode_literals
from __future__ import print_function

from builtins import str

from django.utils.translation import ugettext_lazy as _
from django.utils.text import format_lazy

from lino.api import dd, rt

from lino.utils import join_elems

from lino_xl.lib.courses.desktop import *
from lino_xl.lib.courses.roles import CoursesUser
from lino_xl.lib.contacts.models import PersonDetail

contacts = dd.resolve_app('contacts')

from lino_xl.lib.cal.ui import EntriesByController


Lines.detail_layout = """
    id name ref
    course_area #topic fees_cat fee #options_cat body_template
    #course_type event_type guest_role every_unit every invoicing_policy
    description
    excerpt_title
    courses.CoursesByLine
    """

# Enrolments.detail_layout = """
#     request_date user course
#     pupil places fee option
#     remark amount workflow_buttons
#     confirmation_details invoicing.InvoicingsByGenerator
#     """

Enrolments.detail_layout = """
id course pupil request_date user
start_date end_date #places:8 fee
remark workflow_buttons printed 
confirmation_details invoicing.InvoicingsByGenerator
"""

Activities.params_layout = """topic line user teacher state 
room #can_enroll:10 start_date end_date show_exposed"""

from lino_xl.lib.invoicing.models import InvoicingsByGenerator

InvoicingsByGenerator.column_names = (
    "voucher title qty voucher__voucher_date "
    "voucher__state product__tariff__number_of_events *")


class PendingRequestedEnrolments(PendingRequestedEnrolments):
    column_names = 'request_date course pupil remark user ' \
                   'workflow_buttons'


class EnrolmentsByPupil(EnrolmentsByPupil):
    column_names = 'overview course__state guest_role start_date '\
                   'workflow_buttons *'

    # column_names = 'request_date course user:10 remark ' \
    #                'workflow_buttons *'

    insert_layout = """
    course_area
    course
    # places option
    remark
    request_date user
    """


class EnrolmentsByCourse(EnrolmentsByCourse):
    """The Voga version of :class:`EnrolmentsByCourse
    <lino_xl.lib.courses.ui.EnrolmentsByCourse>`.

    """
    # variable_row_height = True
    column_names = 'request_date pupil guest_role start_date end_date '\
                   'fee ' \
                   'workflow_buttons *'
    insert_layout = """
    pupil guest_role
    remark
    # request_date user
    """

class EnrolmentsAndPaymentsByCourse(Enrolments):
    """Show enrolments of a course together with
    :attr:`payment_info`.

    This is used by `payment_list.body.html`.

    

    """
    master_key = 'course'
    column_names = "pupil_info start_date payment_info"


class EnrolmentsByLifeGroup(EnrolmentsByCourse):
    column_names = 'request_date pupil guest_role '\
                   'remark ' \
                   'workflow_buttons *'
    insert_layout = """
    pupil guest_role
    # places option
    remark
    # request_date user
    """


class EnrolmentsByTherapy(EnrolmentsByLifeGroup):
    column_names = 'pupil guest_role remark ' \
                   'workflow_buttons *'
    
    insert_layout = """
    pupil guest_role
    # places option
    remark
    # request_date user
    """


class EnrolmentsByFee(EnrolmentsByCourse):
    label = _("Enrolments using this fee")
    master_key = "fee"
    column_names = 'course request_date pupil_info start_date end_date '\
                   'remark *'


class EntriesByCourse(EntriesByController):
    """Shows the events linked to this course.
    """
    column_names = "start_date start_time auto_type "\
                   "summary event_type user workflow_buttons *"

    display_mode = "summary"

    @classmethod
    def create_instance(cls, ar, **kw):
        mi = ar.master_instance
        if mi is not None:
            kw['project'] = mi
        return super(EntriesByCourse, cls).create_instance(ar, **kw)

    

class CoursesByLine(CoursesByLine):
    """Like :class:`lino_xl.lib.courses.CoursesByLine`, but with other
    default values in the filter parameters. In Voga we want to see
    only courses for which new enrolments can happen.
    
    TODO: when Lino gets class-based user roles, move this back to the
    library table and show all courses only for users with user_type
    `courses.CourseStaff`.

    """
    # detail_layout = Courses.detail_layout

    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(CoursesByLine, self).param_defaults(ar, **kw)
        kw.update(show_exposed=dd.YesNo.yes)
        return kw


class CourseDetail(CourseDetail):
    main = "general therapy #enrolments calendar sales more"
    general = dd.Panel("""
    ref name partner team
    # client:20 household:20 company:20
    line user teacher workflow_buttons
    enrolments_top
    EnrolmentsByCourse
    """, label=_("General"))

    enrolments_top = '#enrolments_until fee:15 print_actions:15'
    
    therapy = dd.Panel("""
    therapy_domain procurer mandatory translator_type 
    topics.InterestsByController notes.NotesByProject 
    """, label=_("Therapy"))
    
    calendar = dd.Panel("""
    every_unit every max_date max_events
    room start_date end_date start_time end_time
    monday tuesday wednesday thursday friday saturday sunday
    courses.EntriesByCourse
    """, label=_("Appointments"))

    # enrolments = dd.Panel("""
    # """, label=_("Participants"))

    # enrolments_top = 'enrolments_until print_actions:15'

    sales = dd.Panel("""
    # company contact_person
    tariff payment_term paper_type id
    state ending_reason
    invoicing.InvoicingsByGenerator excerpts.ExcerptsByProject
    """, label=_("Invoicing"))

    more = dd.Panel("""
    remark
    #comments.CommentsByRFC cal.TasksByProject
    """, label = _("More"))
    

class LifeGroupDetail(CourseDetail):
    enrolments = dd.Panel("""
    enrolments_top
    EnrolmentsByLifeGroup
    """, label=_("Participants"))


class TherapyDetail(CourseDetail):
    enrolments = dd.Panel("""
    enrolments_top
    EnrolmentsByTherapy
    """, label=_("Participants"))

    # enrolments_top = 'enrolments_until fee:15 print_actions:15'


class Courses(Courses):
    # other groups
    order_by = ['ref', '-start_date', '-start_time']
    column_names = "ref name teacher start_date end_date " \
                   "workflow_buttons *"
    @classmethod
    def param_defaults(self, ar, **kw):
        kw = super(Courses, self).param_defaults(ar, **kw)
        kw.update(show_exposed=dd.YesNo.yes)
        return kw


class LifeGroups(Courses):
    _course_area = CourseAreas.life_groups
    column_names = "ref name teacher partner start_date end_date " \
                   "workflow_buttons *"
    detail_layout = 'courses.LifeGroupDetail'
    insert_layout = """
    line partner #household #teacher
    start_date
    """


class Therapies(Courses):
    # individual therapies
    _course_area = CourseAreas.therapies
    column_names = "ref name teacher partner start_date end_date " \
                   "workflow_buttons *"
    detail_layout = 'courses.TherapyDetail'
    insert_layout = """
    line partner #client #teacher
    start_date
    """

class ActivitiesByPartner(Courses):
    _course_area = None
    master_key = 'partner'
    column_names = "start_date ref line workflow_buttons *"
    order_by = ['-start_date']

# class ActivitiesByClient(Activities):
#     master_key = 'client'

# class ActivitiesByHousehold(Activities):
#     master_key = 'household'    

# class MyCourses(MyCourses):
#     label = _("Therapies managed by me")
#     column_names = "ref name line teacher workflow_buttons *"
#     order_by = ['-ref']

    
class MyCoursesGiven(MyCoursesGiven):
    # label = _("Therapies held by me")
    label = format_lazy(_("My {}"), _("Therapies"))
    column_names = "ref name line workflow_buttons *"
    order_by = ['-ref']
