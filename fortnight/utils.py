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

DT_STRF = '%Y%m%dT%H%M%SZ'


def wrap_in_angle_brackets(value):
    if isinstance(value, unicode):
        return u"<%s>" % value
    elif isinstance(value, str):
        return "<%s>" % value
    else:
        raise TypeError('"%s" is not type str or unicode' % type(value))


def strip_angle_brackets(string):
    return string.strip('<>')
