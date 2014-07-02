#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2014 Paul Durivage <pauldurivage+git@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest
import datetime
from mock import patch

from fortnight import iCalendar
from fortnight import Mailer
from fortnight.exc import ConfigurationError


class TestIcal(unittest.TestCase):
    def setUp(self):
        self.ical = iCalendar()

    def tearDown(self):
        del self.ical

    def test_instantiation(self):
        self.assertTrue(hasattr(self.ical, '_calendar'))
        self.assertTrue(hasattr(self.ical, '_calstr'))

    def test_instantiation_with_config(self):
        def _test_without_dict():
            iCalendar(config=['value'])
        self.assertRaises(TypeError, _test_without_dict)

        config = {
            'method': 'REQUEST'
        }
        ical = iCalendar(config)
        self.assertEqual(ical.method, u'REQUEST')

    def test_set_get_attrs(self):
        loc = 'Easy Street'
        self.ical.location = loc
        self.assertEqual(loc, self.ical.location)

        test_str = '"Thug life"'
        self.ical._arbitrary = test_str
        self.assertEqual(test_str, self.ical._arbitrary)

        multiline = u"""This
is
a
multiline
string"""
        self.ical.summary = multiline
        rejoined = "\n".join(multiline.split())
        self.assertEqual(rejoined, self.ical.summary)

    def test_readonly_properties(self):
        self.assertEqual(self.ical._calendar[u'prodid'], self.ical.prodid)
        self.assertEqual(self.ical._calendar[u'version'], self.ical.version)
        self.assertEqual(self.ical._calendar[u'calscale'], self.ical.calscale)

    def test_set_attr_not_unicode(self):
        self.ical.description = "Not unicode"
        description = self.ical.description
        self.assertIsInstance(description, unicode)

    def test_attr_not_in_defaults(self):
        def _callable():
            self.ical.method = 'arbitrary'
        self.assertRaises(ValueError, _callable)

        def _callable():
            self.ical.status = 'arbitrary'
        self.assertRaises(ValueError, _callable)

    def test_attr_in_defaults(self):
        self.ical.method = 'PUBLISH'
        self.ical.status = 'CONFIRMED'
        self.assertEqual(self.ical.method, 'PUBLISH')
        self.assertEqual(self.ical.status, 'CONFIRMED')
        del self.ical.method
        del self.ical.status
        self.assertIs(self.ical.method, None)
        self.assertIs(self.ical.status, None)

    def test_attr_datetime(self):
        dt_obj = datetime.datetime.now()
        dt_obj = dt_obj.replace(microsecond=0)

        self.ical.dtstamp = dt_obj
        self.ical.dtstart = dt_obj
        self.ical.dtend = dt_obj
        self.assertEqual(dt_obj, self.ical.dtstamp)
        self.assertEqual(dt_obj, self.ical.dtstart)
        self.assertEqual(dt_obj, self.ical.dtend)

        del self.ical.dtstamp
        del self.ical.dtstart
        del self.ical.dtend
        self.assertIs(self.ical.dtstamp, None)
        self.assertIs(self.ical.dtstart, None)
        self.assertIs(self.ical.dtend, None)

        def _callable(attrib):
            setattr(self.ical, attrib, "Moo")
        for item in ['dtstart', 'dtend', 'dtstamp']:
            self.assertRaises(TypeError, _callable, item)

    def test_getattr(self):
        self.assertRaises(AttributeError, getattr, self.ical, '_not_valid')
        self.assertRaises(AttributeError, getattr, self.ical, 'notvalid')

    def test_attrs(self):
        keys = self.ical.attrs
        self.assertIsInstance(keys, list)
        self.assertTrue(keys)

    def test_from_dict(self):
        a_dict = {
            u'method': u'PUBLISH',
            u'dtstart': datetime.datetime.now()
        }
        self.ical.from_dict(a_dict)

        def _callable():
            a_dict['notvalid'] = 'arbitrary'
            self.ical.from_dict(a_dict)
        self.assertRaises(ValueError, _callable)

    def test_to_string(self):
        self.ical.method = u'PUBLISH'
        dtnow = datetime.datetime.now()
        self.ical.dtstart = dtnow
        self.ical.dtend = dtnow
        self.ical.dtstamp = dtnow
        self.ical.organizer_email = u'email@email.com'
        self.ical.attendee_email = u'email@email.com'
        self.ical.status = u'CONFIRMED'
        self.ical.summary = u'FREE TEXT HERE'

        ical_str = self.ical.to_string()
        self.assertIsInstance(ical_str, unicode)

        def _callable():
            self.ical._calendar[u'summary'] = None
            self.ical.to_string()
        self.assertRaises(AttributeError, _callable)


class TestMail(unittest.TestCase):
    def setUp(self):
        _config = {
            'email_to': 'someone@example.com',
            'email_from': 'noreply@mywebstie.com',
            'email_subject': 'Email Subject String',
            'email_body': 'This is the body of an email. Love, Bob',
        }
        self.ical = iCalendar()
        self.ical.method = u'PUBLISH'
        dtnow = datetime.datetime.now()
        self.ical.dtstart = dtnow
        self.ical.dtend = dtnow
        self.ical.dtstamp = dtnow
        self.ical.organizer_email = u'email@email.com'
        self.ical.attendee_email = u'email@email.com'
        self.ical.status = u'CONFIRMED'
        self.ical.summary = u'FREE TEXT HERE'
        self.mailer = Mailer(_config)

    def tearDown(self):
        del self.ical
        del self.mailer

    def test_insantiation(self):
        mail = Mailer(config=dict())
        self.assertTrue(hasattr(mail, '_icalendar'))
        self.assertIs(mail._icalendar, None)
        self.assertIsInstance(mail._config, dict)
        test_dict = {'key': 'value'}
        mail = Mailer(config=test_dict)
        self.assertEqual(mail._config, test_dict)

    def test_attach(self):
        def _callable():
            not_icalendar = int()
            self.mailer.attach(not_icalendar)
        self.assertRaises(TypeError, _callable)
        self.mailer.attach(self.ical)
        self.assertIsInstance(self.mailer._icalendar, iCalendar)

    def test_set_config(self):
        def _callable():
            not_dict = tuple()
            self.mailer.set_config(not_dict)
        self.assertRaises(TypeError, _callable)

    def test_email_to(self):
        email = 'new@email.com'
        self.mailer.email_to = email
        self.assertEqual(self.mailer.email_to, 'new@email.com')
        del self.mailer.email_to
        self.assertFalse(self.mailer.email_to)

    def test_email_from(self):
        email_from = 'new@example.com'
        self.mailer.email_from = email_from
        self.assertEqual(self.mailer.email_from, email_from)
        del self.mailer.email_from
        self.assertFalse(self.mailer.email_from)

    def test_email_body(self):
        email_body = 'Body'
        self.mailer.email_body = email_body
        self.assertEqual(self.mailer.email_body, email_body)
        del self.mailer.email_body
        self.assertFalse(self.mailer.email_body)

    def test_email_subject(self):
        email_subject = 'Subject'
        self.mailer.email_subject = email_subject
        self.assertEqual(self.mailer.email_subject, email_subject)
        del self.mailer.email_subject
        self.assertFalse(self.mailer.email_subject)

    def test_icalendar(self):
        icalendar = self.ical
        self.mailer.icalendar = icalendar
        self.assertEqual(self.mailer.icalendar, icalendar)
        del self.mailer.icalendar
        self.assertFalse(self.mailer.icalendar)

        def _callable():
            not_icalendar = bool()
            self.mailer.icalendar = not_icalendar
        self.assertRaises(TypeError, _callable)

    def test_send_email_missing_content(self):
        self.mailer.attach(self.ical)
        del self.mailer.email_subject
        self.assertRaises(ConfigurationError, self.mailer.send_email)

    def test_send_email_no_ip_and_port(self):
        self.mailer.attach(self.ical)
        self.assertRaises(ConfigurationError, self.mailer.send_email)

    @patch('smtplib.SMTP')
    def test_send_email_with_ip_and_port(self, PatchedSmtplib):
        self.ical.smtplib = PatchedSmtplib
        self.mailer.attach(self.ical)
        self.mailer.smtp_host = 'localhost'
        self.mailer.smtp_port = 25
        result = self.mailer.send_email()
        self.assertIs(result, None)


if __name__ == '__main__':
    unittest.main()
