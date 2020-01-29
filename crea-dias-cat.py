#!/usr/bin/python
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

import pywikibot

for year in ['2018', '2019', '2020']:
    for month, monthnum in [['enero', '01'], ['febrero', '02'], ['marzo', '03'], ['abril', '04'], ['mayo', '05'], ['junio', '06'], ['julio', '07'], ['agosto', '08'], ['septiembre', '09'], ['octubre', '10'], ['noviembre', '11'], ['diciembre', '12']]:
        for day in range(1, 32):
            if month == 'febrero' and day > 28:
                continue
            if month in ['abril', 'junio', 'septiembre', 'noviembre'] and day > 30:
                continue
            print day, month, year
            dianombre = u'%s de %s de %s' % (day, month, year)
            diaiso = u'%s-%s-%02d' % (year, monthnum, day)

            p = pywikibot.Page(pywikibot.Site('15mpedia', '15mpedia'), u'Categoría:%s' % dianombre)
            #if not p.exists():
            output = u"""{{navegación por día categoría|día=%s}}""" % (diaiso)
            p.text = output
            p.save(u"BOT - Creando categoría día")

