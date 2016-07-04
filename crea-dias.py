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

import pywikibot

num2month = {1:'enero', 2:'febrero', 3:'marzo', 4:'abril', 5:'mayo', 6:'junio', 7:'julio', 8:'agosto', 9:'septiembre', 10:'octubre', 11:'noviembre', 12:'diciembre'}

for year in [2017]:
    for month in range(1,13):
        for day in range(1, 32):
            if month == 2 and day > 28:
                continue
            if month in [4, 6, 9, 11] and day > 30:
                continue
            
            title = '%d de %s de %d' % (day, num2month[month], year)
            p = pywikibot.Page(pywikibot.Site('15mpedia', '15mpedia'), title)
            if not p.exists():
                output = u"{{Infobox Día\n|día=%d-%02d-%02d\n}}" % (year, month, day)
                p.text = output
                p.save(u"BOT - Creando día")
            
            redirects = [
                '%d-%02d-%02d' % (year, month, day), 
                '%02d-%02d-%d' % (day, month, year), 
                '%d/%02d/%02d' % (year, month, day), 
                '%02d/%02d/%d' % (day, month, year), 
                '%d %02d %02d' % (year, month, day), 
                '%02d %02d %d' % (day, month, year), 
                '%d de %s de %d' % (day, num2month[month][0].upper()+num2month[month][1:], year), 
                '%d %s %d' % (day, num2month[month], year), 
                '%d %s %d' % (day, num2month[month][0].upper()+num2month[month][1:], year), 
            ]
            for red in redirects:
                redp = pywikibot.Page(pywikibot.Site('15mpedia', '15mpedia'), red)
                output = u"#REDIRECT [[%s]]" % (title)
                redp.text = output
                redp.save(u"BOT - Creando redirección")

