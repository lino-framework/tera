# Copyright 2013-2017 Luc Saffre
# License: BSD (see file COPYING for details)

"""Extends :mod:`lino_xl.lib.courses` for :ref:`tera`.

.. autosummary::
   :toctree:

    models
    desktop
    fixtures.demo

"""


from lino_xl.lib.courses import Plugin
from lino.api import _


class Plugin(Plugin):

    verbose_name = _("Therapies")

    teacher_model = 'users.User'
    """The name of the model to be used for "teachers" (i.e. the person
    who is responsible for a course).

    """
    pupil_model = 'tera.Client'
    """The name of the model to be used for "pupils" (i.e. the persons who
    participate in a course).
    """
    # pupil_name_fields = "pupil__client__name"
    extends_models = ['Enrolment', 'Course', 'Line']
    needs_plugins = [
        'lino_xl.lib.cal', 'lino_xl.lib.invoicing', 'lino_xl.lib.sales']
    # needs_plugins = ['lino_xl.lib.cal', 'lino_cosi.lib.auto.sales']

    def setup_main_menu(self, site, user_type, m):
        m = m.add_menu(self.app_label, self.verbose_name)
        m.add_action('tera.MyClients')
        m.add_action('courses.MyActivities')
        m.add_action('courses.MyCoursesGiven')
        # m.add_action('courses.Pupils')
        # m.add_action('courses.Teachers')
        m.add_separator()
        for ca in site.models.courses.CourseAreas.objects():
            m.add_action(ca.courses_table)
        # m.add_action('courses.Courses')
        # m.add_separator()
        # m.add_action('courses.DraftCourses')
        # m.add_action('courses.InactiveCourses')
        # m.add_action('courses.ActiveCourses')
        # m.add_action('courses.ClosedCourses')
        m.add_separator()
        m.add_action('courses.PendingRequestedEnrolments')
        m.add_action('courses.PendingConfirmedEnrolments')

    def setup_config_menu(self, site, user_type, m):
        m = m.add_menu(self.app_label, self.verbose_name)
        m.add_action('courses.CourseTypes')
        # m.add_separator()
        m.add_action('courses.Topics')
        m.add_action('courses.Lines')
        # m.add_action('courses.TeacherTypes')
        # m.add_action('courses.PupilTypes')
        # m.add_action('courses.Slots')

    def setup_reports_menu(self, site, user_type, m):
        m = m.add_menu(self.app_label, self.verbose_name)
        m.add_action('courses.StatusReport')

