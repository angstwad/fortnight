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

import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

from fortnight import iCalendar
from fortnight.exc import ConfigurationError
from fortnight.utils import strip_angle_brackets


class Mailer(object):
    def __init__(self, config=None):
        self._icalendar = None
        self._config = {}

        if config:
            self.set_config(config)

    def attach(self, icalendar):
        if not isinstance(icalendar, (iCalendar)):
            raise TypeError('%s not of type %s' % (icalendar, type(iCalendar)))
        self._icalendar = icalendar

    def set_config(self, config):
        if not isinstance(config, (dict)):
            raise TypeError('%s not type dict' % config)
        if not hasattr(self, '_config'):
            self._config = {}
        self._config.update(config)

    @property
    def email_to(self):
        return self._config.get('email_to')

    @email_to.setter
    def email_to(self, value):
        self._config['email_to'] = strip_angle_brackets(value)

    @email_to.deleter
    def email_to(self):
        del self._config['email_to']

    @property
    def email_from(self):
        return self._config.get('email_from')

    @email_from.setter
    def email_from(self, value):
        self._config['email_from'] = strip_angle_brackets(value)

    @email_from.deleter
    def email_from(self):
        del self._config['email_from']

    @property
    def email_subject(self):
        return self._config.get('email_subject')

    @email_subject.setter
    def email_subject(self, value):
        self._config['email_subject'] = value

    @email_subject.deleter
    def email_subject(self):
        del self._config['email_subject']

    @property
    def email_body(self):
        return self._config.get('email_body')

    @email_body.setter
    def email_body(self, value):
        self._config['email_body'] = value

    @email_body.deleter
    def email_body(self):
        del self._config['email_body']

    @property
    def icalendar(self):
        return self._icalendar

    @icalendar.setter
    def icalendar(self, value):
        if not isinstance(value, iCalendar):
            raise TypeError
        self._icalendar = value

    @icalendar.deleter
    def icalendar(self):
        self._icalendar = None

    @property
    def smtp_host(self):
        try:
            value = self._config['smtp_host']
        except KeyError:
            raise ConfigurationError('smtp_host not set')
        else:
            return value

    @smtp_host.setter
    def smtp_host(self, value):
        self._config['smtp_host'] = value

    @smtp_host.deleter
    def smtp_host(self):
        del self._config['smtp_host']

    @property
    def smtp_port(self):
        try:
            value = self._config['smtp_port']
        except KeyError:
            return ConfigurationError('smtp_port not set')
        else:
            return value

    @smtp_port.setter
    def smtp_port(self, value):
        self._config['smtp_port'] = value

    @smtp_port.deleter
    def smtp_port(self):
        del self._config['smtp_port']

    def check_config(self):
        try:
            assert self.email_to, 'Missing email_to'
            assert self.email_from, 'Missing email_from'
            assert self.email_subject, 'Missing email_subject'
            assert self.email_body, 'Missing email_body'
            assert self.icalendar and isinstance(self.icalendar, iCalendar),\
                'Missing iCalendar attachment'
        except AssertionError as e:
            raise ConfigurationError(e)

    def send_email(self, ip=None, port=None):
        self.check_config()

        root = MIMEMultipart()
        root['To'] = ",".join(self.email_to)
        root['From'] = self.email_from
        root['Subject'] = self.email_subject

        mix = MIMEMultipart('mixed')
        root.attach(mix)

        alt = MIMEMultipart('alternative')
        mix.attach(alt)

        body = MIMEText(self.email_body, 'plain', _charset='utf-8')
        alt.attach(body)

        if self.icalendar:
            ical_string = self._icalendar.to_string()
            method = self._icalendar.method
            mime_text = MIMEText(ical_string.encode('ascii', 'ignore'),
                                 'calendar; method=%s' % method)
            alt.attach(mime_text)

            mime_application = MIMEApplication(
                ical_string.encode('ascii', 'ignore'),
                'ics; name="invite.ics"')
            mime_application.add_header('Content-Disposition',
                                        'attachment; filename="invite.ics"')
            mix.attach(mime_application)

        parts = mix.as_string().split('MIME-Version: 1.0', 1)
        parts[1] = re.sub('MIME-Version: 1.0\n', '', parts[1])
        new = 'MIME-Version: 1.0\n'.join(parts)

        if not ip or port:
            try:
                ip = self.smtp_host
                port = self.smtp_port
            except ConfigurationError:
                raise ConfigurationError('Specify a port and IP')

        try:
            smtp = smtplib.SMTP(ip, port)
            if not (ip or port):
                smtp.connect()
            smtp.sendmail(self.email_from, self.email_to, new)
            smtp.quit()
        except (smtplib.SMTPHeloError,
                smtplib.SMTPDataError,
                smtplib.SMTPConnectError,
                smtplib.SMTPSenderRefused,
                smtplib.SMTPRecipientsRefused,
                smtplib.SMTPResponseException,
                smtplib.SMTPServerDisconnected,
                smtplib.SMTPAuthenticationError):
            raise
