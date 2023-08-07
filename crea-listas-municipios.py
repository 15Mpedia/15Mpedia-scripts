#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2020-2023 emijrp <emijrp@gmail.com>
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
import sys

site = pywikibot.Site('15mpedia', '15mpedia')
ccaa = {
    u"Andalucíau": [u"Almeríau", u"Cádizu", u"Córdobau", u"Granadau", u"Huelvau", u"Jaénu", u"Málagau", u"Sevillau"], 
    u"Aragónu": [u"Huescau", u"Teruelu", u"Zaragozau"], 
    u"Canariasu": [u"Las Palmasu", u"Santa Cruz de Tenerifeu"], 
    u"Cantabriau": [u"Cantabriau"], 
    u"Castilla-La Manchau": [u"Albaceteu", u"Ciudad Realu", u"Cuencau", u"Guadalajarau", u"Toledou"], 
    u"Castilla y Leónu": [u"Ávilau", u"Burgosu", u"Leónu", u"Palenciau", u"Salamancau", u"Segoviau", u"Soriau", u"Valladolidu", u"Zamorau"], 
    u"Cataluñau": [u"Barcelonau", u"Gironau", u"Lleidau", u"Tarragonau"], 
    u"Comunidad de Madridu": [u"Madridu"], 
    u"Comunidad Foral de Navarrau": [u"Navarrau"], 
    u"Comunidad Valencianau": [u"Alicanteu", u"Castellónu", u"Valenciau"], 
    u"Extremadurau": [u"Badajozu", u"Cáceresu"], 
    u"Galiciau": [u"A Coruñau", u"Lugou", u"Ourenseu", u"Pontevedrau"], 
    u"Islas Balearesu": [u"Balearesu"], 
    u"La Riojau": [u"La Riojau"], 
    u"País Vascou": [u"Álavau", u"Gipuzkoau", u"Vizcayau"], 
    u"Principado de Asturiasu": [u"Asturiasu"], 
    u"Región de Murciau": [u"Murciau"], 
}

for comunidad, provincias in ccaa.items():
    de = 'de'
    if comunidad == 'Islas Baleares':
        de = 'de las'
    elif comunidad in ['País Vasco', 'Principado de Asturias']:
        de = 'del'
    elif comunidad in ['Comunidad Foral de Navarra', 'Comunidad de Madrid', 'Comunidad Valenciana', 'Región de Murcia']:
        de = 'de la'
    
    """
    for por in ["altitud", "población", "superficie"]:
        wtitle = "Lista de municipios %s %s por %s" % (de, comunidad, por)
        wtext = "{{Lista de municipios por lugar|país=España|comunidad autónoma=%s|sort=%s}}" % (comunidad, por)
        page = pywikibot.Page(site, wtitle)
        if False and page.exists():
            print("La pagina %s ya existe" % (wtitle))
        else:
            page.text = wtext
            page.save("BOT - Creando lista de comunidad autónoma", botflag=False)
        
        if len(provincias) > 1:
            for provincia in provincias:
                wtitle = "Lista de municipios de la provincia de %s por %s" % (provincia, por)
                wtext = "{{Lista de municipios por lugar|país=España|comunidad autónoma=%s|provincia=Provincia de %s|sort=%s}}" % (comunidad, provincia, por)
                page = pywikibot.Page(site, wtitle)
                if False and page.exists():
                    print("La pagina %s ya existe" % (wtitle))
                else:
                    page.text = wtext
                    page.save("BOT - Creando lista de provincia", botflag=False)
        else:
            wtitle = "Lista de municipios de la provincia de %s por %s" % (provincias[0], por)
            redtitle = "Lista de municipios %s %s por %s" % (de, comunidad, por)
            wtext = u"#REDIRECT [[%s]]" % (redtitle)
            page = pywikibot.Page(site, wtitle)
            if page.exists():
                print("La pagina %s ya existe" % (wtitle))
            else:
                page.text = wtext
                page.save("BOT - Creando redirect hacia [[%s]]" % (redtitle), botflag=False)
    """
    
    for por in ["población"]:
        for year in range(2001, 2023):
            wtitle = u"Lista de municipios %s %s por %s (%s)" % (de, comunidad, por, year)
            wtext = u"{{Lista de municipios por lugar|país=España|comunidad autónoma=%s|año=%s|sort=%s}}" % (comunidad, year, por)
            page = pywikibot.Page(site, wtitle)
            if False and page.exists():
                print(u"La pagina %s ya existe" % (wtitle))
            else:
                page.text = wtext
                page.save(u"BOT - Creando lista de comunidad autónoma", botflag=False)
            
            if len(provincias) > 1:
                for provincia in provincias:
                    wtitle = u"Lista de municipios de la provincia de %s por %s (%s)" % (provincia, por, year)
                    wtext = u"{{Lista de municipios por lugar|país=España|comunidad autónoma=%s|provincia=Provincia de %s|año=%s|sort=%s}}" % (comunidad, provincia, year, por)
                    page = pywikibot.Page(site, wtitle)
                    if False and page.exists():
                        print(u"La pagina %s ya existe" % (wtitle))
                    else:
                        page.text = wtext
                        page.save(u"BOT - Creando lista de provincia", botflag=False)
            else:
                wtitle = u"Lista de municipios de la provincia de %s por %s (%s)" % (provincias[0], por, year)
                redtitle = u"Lista de municipios %s %s por %s (%s)" % (de, comunidad, por, year)
                wtext = u"#REDIRECT [[%s]]" % (redtitle)
                page = pywikibot.Page(site, wtitle)
                if page.exists():
                    print(u"La pagina %s ya existe" % (wtitle))
                else:
                    page.text = wtext
                    page.save(u"BOT - Creando redirect hacia [[%s]]" % (redtitle), botflag=False)


