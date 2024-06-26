#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2015-2020 emijrp <emijrp@gmail.com>
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

#for year in range(1900, 2020+1):
for year in range(2020, 2021+1):
    for month, monthnum in [['enero', '01'], ['febrero', '02'], ['marzo', '03'], ['abril', '04'], ['mayo', '05'], ['junio', '06'], ['julio', '07'], ['agosto', '08'], ['septiembre', '09'], ['octubre', '10'], ['noviembre', '11'], ['diciembre', '12']]:
        print(month, year)
        mesnombre = '%s de %s' % (month, year)
        mesiso = '%s-%s' % (year, monthnum)
        
        p = pywikibot.Page(pywikibot.Site('15mpedia', '15mpedia'), '%s' % mesnombre)
        if not p.exists():
            output = """{{Infobox Mes\n|mes=%s\n}}""" % (mesiso)
            p.text = output
            p.save("BOT - Creando mes")
        
        p = pywikibot.Page(pywikibot.Site('15mpedia', '15mpedia'), 'Categoría:%s' % mesnombre)
        if not p.exists():
            output = """{{navegación por mes categoría|mes=%s}}""" % (mesiso)
            p.text = output
            p.save("BOT - Creando categoría mes")

