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

#This script generates redirects for wiki articles
#removing uppercase, accents and other symbols

import pywikibot
import pywikibot.pagegenerators as pagegenerators

def main():
    site = pywikibot.Site('15mpedia', '15mpedia')
    category = pywikibot.Category(site, 'Categoría:Municipios de España')
    gen = pagegenerators.CategorizedPageGenerator(category=category, start='', namespaces=[0])
    pre = pagegenerators.PreloadingGenerator(gen, pageNumber=250)
    
    for page in pre:
        if not page.exists() or page.isRedirectPage() or page.title().startswith('Lista'):
            continue

        municat = pywikibot.Page(site, 'Categoría:%s' % (page.title()))
        if not municat.exists():
            municat.text = '{{Categoría municipio}}'
            municat.save('BOT - Creando categoría de municipio')

if __name__ == '__main__':
    main()
