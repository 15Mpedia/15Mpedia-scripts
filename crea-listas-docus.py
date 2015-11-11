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

for year in range(1930, 2020):
    title = u'Lista de documentales de %d' % (year)
    p = pywikibot.Page(pywikibot.Site('15mpedia', '15mpedia'), title)
    output = u"{{Lista de documentales por año|año=%s}}" % (year)
    p.text = output
    p.save(u"BOT - Creando lista")
    
    title = u'Lista de documentales en %d' % (year)
    p = pywikibot.Page(pywikibot.Site('15mpedia', '15mpedia'), title)
    output = u"#redirect [[Lista de documentales de %s]]" % (year)
    p.text = output
    p.save(u"BOT - Creando redirección")
    
    title = u'Categoría:Documentales de %d' % (year)
    p = pywikibot.Page(pywikibot.Site('15mpedia', '15mpedia'), title)
    output = u"{{Categoría documentales por año|año=%s}}" % (year)
    p.text = output
    p.save(u"BOT - Creando categoría")

    title = u'Lista de películas de %d' % (year)
    p = pywikibot.Page(pywikibot.Site('15mpedia', '15mpedia'), title)
    output = u"{{Lista de películas por año|año=%s}}" % (year)
    p.text = output
    p.save(u"BOT - Creando lista")
    
    title = u'Lista de películas en %d' % (year)
    p = pywikibot.Page(pywikibot.Site('15mpedia', '15mpedia'), title)
    output = u"#redirect [[Lista de películas de %s]]" % (year)
    p.text = output
    p.save(u"BOT - Creando redirección")
    
    title = u'Categoría:Películas de %d' % (year)
    p = pywikibot.Page(pywikibot.Site('15mpedia', '15mpedia'), title)
    output = u"{{Categoría películas por año|año=%s}}" % (year)
    p.text = output
    p.save(u"BOT - Creando categoría")

