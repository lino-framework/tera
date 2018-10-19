# -*- coding: UTF-8 -*-
# Copyright 2013-2017 Luc Saffre
# License: BSD (see file COPYING for details)

"""
Desktop design for this plugin.

"""

from __future__ import unicode_literals
from __future__ import print_function

from builtins import str

from django.utils.translation import ugettext_lazy as _

from lino.api import dd, rt

from lino.utils import join_elems

from lino_xl.lib.courses.desktop import *
from lino_xl.lib.courses.roles import CoursesUser
from lino_xl.lib.contacts.models import PersonDetail

contacts = dd.resolve_app('contacts')

from lino_xl.lib.cal.ui import EntriesByController


# class CourseTypes(dd.Table):
#     model = 'courses.CourseType'
#     required_roles = dd.login_required(CoursesUser)
#     detail_layout = """
#     id name
#     courses.LinesByType
#     """


Lines.detail_layout = """
    id name ref
    course_area #topic fees_cat fee options_cat body_template
    #course_type event_type guest_role every_unit every
    description
    excerpt_title
    courses.CoursesByLine
    """


# Enrolments.detail_layout = """
#     request_date user course
#     pupil places fee option
#     remark amount workflow_buttons
#     confirmation_details invoicing.InvoicingsByInvoiceable
#     """

Enrolments.detail_layout = """
id course pupil request_date user
start_date end_date #places:8 fee
remark workflow_buttons printed 
confirmation_details invoicing.InvoicingsByInvoiceable
"""


from lino_xl.lib.invoicing.models import InvoicingsByInvoiceable

InvoicingsByInvoiceable.column_names = (
    "voucher title qty voucher__voucher_date "
    "voucher__state product__number_of_events *")


class PendingRequestedEnrolments(PendingRequestedEnrolments):
    column_names = 'request_date course pupil remark user ' \
                   'workflow_buttons'


class EnrolmentsByPupil(EnrolmentsByPupil):
    column_names = 'overview start_date '\
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
    column_names = 'request_date pupil start_date end_date '\
                   'remark fee ' \
                   'workflow_buttons *'


class EnrolmentsByFee(EnrolmentsByCourse):
    label = _("Enrolments using this fee")
    master_key = "fee"
    column_names = 'course request_date pupil_info start_date end_date '\
                   'remark *'


class EntriesByCourse(EntriesByController):
    """Shows the events linked to this course.
    """
    column_names = "start_date auto_type workflow_buttons "\
                   "start_time end_time room summary *"

    display_mode = "summary"


class CourseDetail(CourseDetail):
    main = "general enrolments calendar notes more"
    general = dd.Panel("""
    ref name #household:20 partner client:20
    therapy_domain procurer mandatory translator_type 
    line user teacher workflow_buttons
    remark topics.InterestsByController
    """, label=_("General"))

    calendar = dd.Panel("""
    every_unit every max_date max_events
    room start_date end_date start_time end_time
    monday tuesday wednesday thursday friday saturday sunday
    courses.EntriesByCourse
    """, label=_("Appointments"))

    enrolments = dd.Panel("""
    enrolments_top
    EnrolmentsByCourse
    """, label=_("Participants"))

    enrolments_top = 'enrolments_until print_actions:15'

    notes = dd.Panel("""
    notes.NotesByProject
    #comments.CommentsByRFC cal.TasksByProject
    """, label = _("Notes"))

    more = dd.Panel("""
    # company contact_person
    tariff payment_term paper_type id
    state ending_reason
    invoicing.InvoicingsByInvoiceable excerpts.ExcerptsByProject
    """, label=_("More"))


# Course.detail_layout_class = CourseDetail
# Courses._course_area = CourseAreas.default
Courses.order_by = ['ref', '-start_date', '-start_time']
Courses.column_names = "ref name start_date enrolments_until line teacher " \
                       "workflow_buttons *"



# class Courses(Courses):
#     # detail_layout = CourseDetail()
#     order_by = ['ref', '-start_date', '-start_time']
#     column_names = "ref start_date enrolments_until line room teacher " \
#                    "workflow_buttons *"


# @dd.receiver(dd.pre_analyze)
# def customize_courses(sender, **kw):
#     sender.modules.courses.Courses.set_detail_layout(CourseDetail())

if False:

    # Exception: Cannot reuse detail_layout of <class
    # 'lino_xl.lib.courses.models.CoursesByTeacher'> for <class
    # 'lino_xl.lib.courses.models.CoursesBySlot'>

    class Courses(Courses):

        parameters = dict(Courses.parameters,
            city=dd.ForeignKey('countries.Place', blank=True, null=True))

        params_layout = """line city teacher user state active:10"""

        @classmethod
        def get_request_queryset(self, ar):
            qs = super(Courses, self).get_request_queryset(ar)
            if ar.param_values.city:
                flt = Q(room__isnull=True)
                flt |= Q(room__company__city=ar.param_values.city)
                qs = qs.filter(flt)
            return qs

        @classmethod
        def get_title_tags(self, ar):
            for t in super(Courses, self).get_title_tags(ar):
                yield t
            if ar.param_values.city:
                yield _("in %s") % ar.param_values.city

        @dd.chooser()
        def city_choices(cls):
            Place = rt.models.countries.Place
            Room = rt.models.cal.Room
            places = set([
                obj.company.city.id
                for obj in Room.objects.filter(company__isnull=False)])
            # logger.info("20140822 city_choices %s", places)
            return Place.objects.filter(id__in=places)

    class SuggestedCoursesByPupil(SuggestedCoursesByPupil):
        button_text = _("Suggestions")
        params_layout = 'line city teacher active'

        @classmethod
        def param_defaults(self, ar, **kw):
            kw = super(SuggestedCoursesByPupil, self).param_defaults(ar, **kw)
            # kw.update(active=dd.YesNo.yes)
            pupil = ar.master_instance
            if pupil and pupil.city:
                kw.update(city=pupil.city)
            return kw


# class CoursesByTopic(CoursesByTopic):
#     """Shows the courses of a given topic.

#     This is used both in the detail window of a topic and in
#     :class:`StatusReport`.

#     """
#     order_by = ["ref"]
#     column_names = "overview weekdays_text:10 times_text:10 * "

#     # detail_layout = Courses.detail_layout

#     @classmethod
#     def param_defaults(self, ar, **kw):
#         kw = super(CoursesByTopic, self).param_defaults(ar, **kw)
#         kw.update(state=CourseStates.active)
#         kw.update(can_enroll=dd.YesNo.yes)
#         return kw


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
        kw.update(state=CourseStates.active)
        kw.update(can_enroll=dd.YesNo.yes)
        return kw


# class LinesByType(Lines):
#     master_key = 'course_type'


# class ActiveCourses(ActiveCourses):
#     column_names = 'info max_places enrolments teacher line room *'
#     hide_sums = True




class EnrolmentsAndPaymentsByCourse(Enrolments):
    """Show enrolments of a course together with
    :attr:`payment_info`.

    This is used by `payment_list.body.html`.

    

    """
    master_key = 'course'
    column_names = "pupil_info start_date payment_info"


class EnrolmentsByLifeGroup(EnrolmentsByCourse):
    column_names = 'request_date pupil '\
                   'remark fee ' \
                   'workflow_buttons *'
    insert_layout = """
    pupil
    places option
    remark
    request_date user
    """


class EnrolmentsByTherapy(EnrolmentsByLifeGroup):
    pass


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

    enrolments_top = 'enrolments_until fee:15 print_actions:15'

class LifeGroups(Courses):
    _course_area = CourseAreas.life_groups
    column_names = "ref name start_date enrolments_until line " \
                   "workflow_buttons *"
    detail_layout = 'courses.LifeGroupDetail'
    insert_layout = """
    line partner #household #teacher
    start_date
    """


class Therapies(Courses):
    _course_area = CourseAreas.therapies
    column_names = "ref name start_date end_date enrolments_until line " \
                   "workflow_buttons *"
    detail_layout = 'courses.TherapyDetail'
    insert_layout = """
    line partner #client #teacher
    start_date
    """

class ActivitiesByPartner(Activities):
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

from django.utils.text import format_lazy
    
class MyCoursesGiven(MyCoursesGiven):
    # label = _("Therapies held by me")
    label = format_lazy(_("My {}"), _("Therapies"))
    column_names = "ref name line workflow_buttons *"
    order_by = ['-ref']
