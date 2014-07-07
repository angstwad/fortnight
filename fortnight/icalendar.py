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

import uuid
import datetime
import defaults
from datetime import datetime as DateTime

from fortnight.utils import DT_STRF, strip_angle_brackets


class iCalendar(object):
    def __init__(self, config=None):
        """ Represents an iCalendar object.  Has attributes must be assigned
        non-None values before invoking the :py:meth:`to_string`
        method.

        :param config: A dict containing configuration information
        """
        self._calendar = {
            u'prodid': u'Microsoft Exchange Server 2010',
            u'version': u'2.0',
            u'calscale': u'GREGORIAN',
            u'method': None,
            u'dtstart': None,
            u'dtend': None,
            u'dtstamp': None,
            u'organizer_email': None,
            u'uid': uuid.uuid4().hex,
            u'uid_fqdn': '',
            u'attendee_email': None,
            u'description': '',
            u'location': '',
            u'status': None,
            u'summary': None,
        }
        if config:
            self.from_dict(config)

        self._calstr = u"""BEGIN:VCALENDAR
PRODID:{prodid}
VERSION:{version}
CALSCALE:{calscale}
METHOD:{method}
BEGIN:VEVENT
DTSTART:{dtstart}
DTEND:{dtend}
DTSTAMP:{dtstamp}
ORGANIZER;CN={organizer_email}:mailto:{organizer_email}
UID:{uid}@{uid_fqdn}
 ATTENDEE;CUTYPE=INDIVIDUAL;ROLE=REQ-PARTICIPANT;PARTSTAT=NEEDS-ACTION;RSVP=TRUE
 ;CN={attendee_email}:MAILTO:{attendee_email}
CREATED:{dtstamp}
DESCRIPTION:{description}
LAST-MODIFIED:{dtstamp}
LOCATION:{location}
SEQUENCE:0
STATUS:{status}
SUMMARY:{summary}
TRANSP:TRANSPARENT
END:VEVENT
END:VCALENDAR
"""

    @property
    def prodid(self):
        return self._calendar[u'prodid']

    @property
    def version(self):
        return self._calendar[u'version']

    @property
    def calscale(self):
        return self._calendar[u'calscale']

    @property
    def method(self):
        return self._calendar[u'method']

    @method.setter
    def method(self, value):
        value = value.upper()
        if value not in defaults.METHODS:
            raise ValueError('%s not in %s' % (value, defaults.METHODS))
        self._calendar[u'method'] = unicode(value)

    @method.deleter
    def method(self):
        self._calendar[u'method'] = None

    @property
    def dtstart(self):
        try:
            return DateTime.strptime(self._calendar[u'dtstart'], DT_STRF)
        except TypeError:
            pass

    @dtstart.setter
    def dtstart(self, value):
        if not isinstance(value, datetime.datetime):
            raise TypeError('%s is not of type '
                            'datetime.datetime' % value)
        self._calendar[u'dtstart'] = value.strftime(DT_STRF)

    @dtstart.deleter
    def dtstart(self):
        self._calendar[u'dtstart'] = None

    @property
    def dtend(self):
        try:
            return DateTime.strptime(self._calendar[u'dtend'], DT_STRF)
        except TypeError:
            pass

    @dtend.setter
    def dtend(self, value):
        if not isinstance(value, datetime.datetime):
            raise TypeError('%s is not of type '
                            'datetime.datetime' % value)
        self._calendar[u'dtend'] = value.strftime(DT_STRF)

    @dtend.deleter
    def dtend(self):
        self._calendar[u'dtend'] = None

    @property
    def dtstamp(self):
        try:
            return DateTime.strptime(self._calendar[u'dtstamp'], DT_STRF)
        except TypeError:
            pass

    @dtstamp.setter
    def dtstamp(self, value):
        if not isinstance(value, datetime.datetime):
            raise TypeError('%s is not of type '
                            'datetime.datetime' % value)
        self._calendar[u'dtstamp'] = value.strftime(DT_STRF)

    @dtstamp.deleter
    def dtstamp(self):
        self._calendar[u'dtstamp'] = None

    @property
    def organizer_email(self):
        if self._calendar[u'organizer_email']:
            return self._calendar[u'organizer_email']

    @organizer_email.setter
    def organizer_email(self, value):
        self._calendar[u'organizer_email'] = unicode(
            strip_angle_brackets(value))

    @organizer_email.deleter
    def organizer_email(self):
        self._calendar[u'organizer_email'] = None

    @property
    def uid(self):
        return self._calendar[u'uid']

    @uid.setter
    def uid(self, value):
        self._calendar[u'uid'] = unicode(value)

    @property
    def uid_fqdn(self):
        return self._calendar[u'uid_fqdn']

    @uid_fqdn.setter
    def uid_fqdn(self, value):
        self._calendar[u'uid_fqdn'] = unicode(value)

    @uid_fqdn.deleter
    def uid_fqdn(self):
        self._calendar[u'uid_fqdn'] = u''

    @property
    def attendee_email(self):
        if self._calendar[u'attendee_email']:
            return self._calendar[u'attendee_email']

    @attendee_email.setter
    def attendee_email(self, value):
        self._calendar[u'attendee_email'] = unicode(
            strip_angle_brackets(value))

    @attendee_email.deleter
    def attendee_email(self):
        self._calendar[u'attendee_email'] = None

    @property
    def description(self):
        return self._calendar[u'description']

    @description.setter
    def description(self, value):
        self._calendar[u'description'] = unicode(value)

    @description.deleter
    def description(self):
        self._calendar[u'description'] = u''

    @property
    def location(self):
        return self._calendar[u'location']

    @location.setter
    def location(self, value):
        self._calendar[u'location'] = unicode(value)

    @location.deleter
    def location(self):
        self._calendar[u'location'] = u''

    @property
    def status(self):
        return self._calendar[u'status']

    @status.setter
    def status(self, value):
        value = value.upper()
        if value not in defaults.STATUS:
            raise ValueError('%s not in %s' % (value, defaults.STATUS))
        self._calendar[u'status'] = unicode(value)

    @status.deleter
    def status(self):
        self._calendar[u'status'] = None

    @property
    def summary(self):
        return self._calendar[u'summary']

    @summary.setter
    def summary(self, value):
        self._calendar[u'summary'] = unicode(value)

    @summary.deleter
    def summary(self):
        self._calendar[u'summary'] = None

    @property
    def attrs(self):
        """ Attributes that the iCalendar object uses for when creating an
        iCalendar event.

        :return: list of attribute names as strings
        """
        return self._calendar.keys()

    def from_dict(self, config):
        """ Configure an iCalendar object from a dictionary

        :param config: Dictionary of values with which to configure iCalendar
        event. All the possible keys can be used by looking up the
        iCalendar.attrs property
        :raise ValueError: If config is not a dictionary
        """
        if not isinstance(config, dict):
            raise TypeError('"%s" is not type dict' % type(config))
        for key, val in config.items():
            if key not in self._calendar.keys():
                raise ValueError('"%s" not a valid key' % key)
            else:
                setattr(self, key, val)

    def to_string(self):
        """ Serializes an iCalendar event to unicode

        :return: Unicode
        :raise AttributeError: If required attributes are None
        """
        if None in self._calendar.values():
            for key, val in self._calendar.items():
                if val is None:
                    raise AttributeError(
                        'Attribute "%s" should not be None' % key)
        return self._calstr.format(**self._calendar)
