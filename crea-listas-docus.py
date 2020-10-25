#!/usr/bin/env python
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

site = pywikibot.Site('15mpedia', '15mpedia')

for year in range(1848, 2021):
    title = 'Lista de obras de %d' % (year)
    p = pywikibot.Page(site, title)
    output = "{{Lista de obras por año|año=%d}}" % (year)
    p.text = output
    p.save("BOT - Creando lista")
    
    title = 'Categoría:Obras de %d' % (year)
    p = pywikibot.Page(site, title)
    output = "{{Categoría obras por año|año=%d}}" % (year)
    p.text = output
    p.save("BOT - Creando categoría")

"""
for year in range(1930, 2021):
    title = 'Cine de %d' % (year)
    p = pywikibot.Page(site, title)
    output = "{{Cine por año|año=%d}}" % (year)
    p.text = output
    p.save("BOT - Creando página")"""

"""title = u'Lista de documentales de %d' % (year)
    p = pywikibot.Page(site, title)
    output = u"{{Lista de documentales por año|año=%d}}" % (year)
    p.text = output
    p.save("BOT - Creando lista")
    
    title = u'Lista de documentales en %d' % (year)
    p = pywikibot.Page(site, title)
    output = u"#redirect [[Lista de documentales de %d]]" % (year)
    p.text = output
    p.save("BOT - Creando redirección")
    
    title = u'Categoría:Documentales de %d' % (year)
    p = pywikibot.Page(site, title)
    output = u"{{Categoría documentales por año|año=%d}}" % (year)
    p.text = output
    p.save("BOT - Creando categoría")

    title = u'Lista de películas de %d' % (year)
    p = pywikibot.Page(site, title)
    output = u"{{Lista de películas por año|año=%d}}" % (year)
    p.text = output
    p.save("BOT - Creando lista")
    
    title = u'Lista de películas en %d' % (year)
    p = pywikibot.Page(site, title)
    output = u"#redirect [[Lista de películas de %d]]" % (year)
    p.text = output
    p.save("BOT - Creando redirección")
    
    title = u'Categoría:Películas de %d' % (year)
    p = pywikibot.Page(site, title)
    output = u"{{Categoría películas por año|año=%d}}" % (year)
    p.text = output
    p.save("BOT - Creando categoría")"""

"""
for year in range(1848, 2021):
    title = 'Literatura de %d' % (year)
    p = pywikibot.Page(site, title)
    output = "{{Literatura por año|año=%d}}" % (year)
    p.text = output
    p.save("BOT - Creando página")


    title = u'Lista de libros de %d' % (year)
    p = pywikibot.Page(site, title)
    output = u"{{Lista de libros por año|año=%d}}" % (year)
    p.text = output
    p.save("BOT - Creando lista")
    
    title = u'Lista de libros en %d' % (year)
    p = pywikibot.Page(site, title)
    output = u"#redirect [[Lista de libros de %d]]" % (year)
    p.text = output
    p.save("BOT - Creando redirección")
    
    title = u'Categoría:Libros de %d' % (year)
    p = pywikibot.Page(site, title)
    output = u"{{Categoría libros por año|año=%d}}" % (year)
    p.text = output
    p.save("BOT - Creando categoría")
"""
"""
for year in range(1780, 2021):
    title = 'Plantilla:%d' % (year)
    p = pywikibot.Page(site, title)
    output = "{{Navbox Año|año=%d}}<noinclude>[[Categoría:Plantillas de navegación]]</noinclude>" % (year)
    p.text = output
    p.save("BOT - Creando plantilla")
"""
