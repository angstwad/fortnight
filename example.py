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

import datetime
from datetime import datetime as DateTime
from fortnight import Mailer, iCalendar

cal = None
mail = None


def config_ical():
    start = DateTime(2014, 12, 1, 7, 30)
    end = datetime.timedelta(days=7) + start
    now = DateTime.now()

    config = {
        'method': 'REQUEST',
        'organizer_email': 'organizer@example.com',
        'attendee_email': 'attendee@example.com',
        'description': 'This is an iCalendar Event Description',
        'dtstart': start,
        'dtend': end,
        'dtstamp': now,
        'location': 'The Moon',
        'status': 'TENTATIVE',
        'summary': 'This is an iCalendar Event Summary'
    }
    global cal
    cal = iCalendar(config)


def config_mail():
    config = {
        'email_to': 'attendee@example.com',
        'email_from': 'organizer@example.com',
        'email_subject': 'This is the subject of the email',
        'email_body': 'This is the body of the email',
        'smtp_host': 'vm.local',
        'smtp_port': 25,
    }
    global mail
    mail = Mailer(config)


def main():
    config_ical()
    config_mail()

    mail.attach(cal)
    mail.send_email()


if __name__ == '__main__':
    main()