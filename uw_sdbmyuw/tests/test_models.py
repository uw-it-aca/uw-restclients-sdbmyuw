from unittest import TestCase
from uw_sdbmyuw.models import (has_no_ug_app, set_campus,
                               set_data, ApplicationStatus)


class ModelsTest(TestCase):

    def test_set_campus(self):
        status = ApplicationStatus()
        self.assertFalse(status.is_bothell)
        self.assertFalse(status.is_seattle)
        self.assertFalse(status.is_tacoma)
        html_data = "UW Bothell Campus Applications"
        set_campus(status, html_data)
        self.assertTrue(status.is_bothell)

        html_data = "UW Seattle Applications"
        set_campus(status, html_data)
        self.assertTrue(status.is_seattle)

        html_data = "UW Tacoma Campus Applications"
        set_campus(status, html_data)
        self.assertTrue(status.is_tacoma)

    def test_has_no_ug_app(self):
        html_data = ('The UW does not have an active undergraduate ' +
                     'application on file for you.')
        self.assertTrue(has_no_ug_app(html_data))
        status = ApplicationStatus.create(html_data)
        self.assertTrue(status.no_ug_app)

    def test_set_data(self):
        html_data = '<b>UW Seattle Campus Applications:</b>' +\
                    'Freshman Application: autumn quarter 2017'
        status = ApplicationStatus()
        set_data(status, html_data)
        self.assertEqual(status.json_data(),
                         {'is_freshman': True,
                          'is_seattle': True,
                          'is_bothell': False,
                          'is_tacoma': False,
                          'year': 2017,
                          'is_transfer': False,
                          'is_returning': False,
                          'is_ug_non_matriculated': False,
                          'quarter': 'autumn',
                          'is_international_post_bac': False,
                          'no_ug_app': False})
        html_data = '<b>UW Bothell Campus Applications:</b>' +\
                    'Transfer Application: autumn quarter 2016'
        status = ApplicationStatus()
        set_data(status, html_data)
        self.assertEqual(status.json_data(),
                         {'is_freshman': False,
                          'is_seattle': False,
                          'is_bothell': True,
                          'is_tacoma': False,
                          'year': 2016,
                          'is_transfer': True,
                          'is_returning': False,
                          'is_ug_non_matriculated': False,
                          'quarter': 'autumn',
                          'is_international_post_bac': False,
                          'no_ug_app': False})
        html_data = 'on your returning student application to the UW Seattle,'
        status = ApplicationStatus()
        set_data(status, html_data)
        self.assertTrue(status.is_returning)
        self.assertTrue(status.is_seattle)
        html_data = '<b>UW Tacoma Campus Applications:</b>' +\
                    'International Postbaccalaureate Application: ' +\
                    'autumn quarter 2017'
        set_data(status, html_data)
        self.assertTrue(status.is_international_post_bac)
        self.assertTrue(status.is_tacoma)
        self.assertEqual(status.quarter, 'autumn')
        self.assertEqual(status.year, 2017)
        html_data = '<b>UW Bothell Campus Applications:</b>' +\
                    'Nonmatriculated Application: winter quarter 2018'
        set_data(status, html_data)
        self.assertTrue(status.is_ug_non_matriculated)
        self.assertTrue(status.is_bothell)
        self.assertEqual(status.quarter, 'winter')
        self.assertEqual(status.year, 2018)
        status = ApplicationStatus.create(html_data)
        self.assertIsNotNone(status.json_data())
        self.assertIsNotNone(status.__str__())
