#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2015 emijrp <emijrp@gmail.com>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import wikipedia

for month, monthnum in [['enero', '01'], ['febrero', '02'], ['marzo', '03'], ['abril', '04'], ['mayo', '05'], ['junio', '06'], ['julio', '07'], ['agosto', '08'], ['septiembre', '09'], ['octubre', '10'], ['noviembre', '11'], ['diciembre', '12']]:
    for day in range(1, 32):
        if month == 'febrero' and day > 28:
            continue
        if month in ['abril', 'junio', 'septiembre', 'noviembre'] and day > 30:
            continue
        print day, month
        dianombre = u'%s de %s' % (day, month)
        dianombre2 = u'%s %s' % (day, month)
        dianombremayus = u'%s de %s' % (day, month[0].upper()+month[1:])
        dianombremayus2 = u'%s %s' % (day, month[0].upper()+month[1:])

        p = wikipedia.Page(wikipedia.Site('15mpedia', '15mpedia'), dianombre)
        if not p.exists():
            output = u"""{{desambiguación día}}"""
            p.put(output, u"BOT - Creando día")
        r = wikipedia.Page(wikipedia.Site('15mpedia', '15mpedia'), dianombre2)
        if not r.exists():
            output = u'#REDIRECT [[%s]]' % (dianombre)
            r.put(output, u'BOT - Creando redirección')
        r = wikipedia.Page(wikipedia.Site('15mpedia', '15mpedia'), dianombremayus)
        if not r.exists():
            output = u'#REDIRECT [[%s]]' % (dianombre)
            r.put(output, u'BOT - Creando redirección')
        r = wikipedia.Page(wikipedia.Site('15mpedia', '15mpedia'), dianombremayus2)
        if not r.exists():
            output = u'#REDIRECT [[%s]]' % (dianombre)
            r.put(output, u'BOT - Creando redirección')
