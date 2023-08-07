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
    u"Andalucía": [u"Almería", u"Cádiz", u"Córdoba", u"Granada", u"Huelva", u"Jaén", u"Málaga", u"Sevilla"], 
    u"Aragón": [u"Huesca", u"Teruel", u"Zaragoza"], 
    u"Canarias": [u"Las Palmas", u"Santa Cruz de Tenerife"], 
    u"Cantabria": [u"Cantabria"], 
    u"Castilla-La Mancha": [u"Albacete", u"Ciudad Real", u"Cuenca", u"Guadalajara", u"Toledo"], 
    u"Castilla y León": [u"Ávila", u"Burgos", u"León", u"Palencia", u"Salamanca", u"Segovia", u"Soria", u"Valladolid", u"Zamora"], 
    u"Cataluña": [u"Barcelona", u"Girona", u"Lleida", u"Tarragona"], 
    u"Comunidad de Madrid": [u"Madrid"], 
    u"Comunidad Foral de Navarra": [u"Navarra"], 
    u"Comunidad Valenciana": [u"Alicante", u"Castellón", u"Valencia"], 
    u"Extremadura": [u"Badajoz", u"Cáceres"], 
    u"Galicia": [u"A Coruña", u"Lugo", u"Ourense", u"Pontevedra"], 
    u"Islas Baleares": [u"Baleares"], 
    u"La Rioja": [u"La Rioja"], 
    u"País Vasco": [u"Álava", u"Gipuzkoa", u"Vizcaya"], 
    u"Principado de Asturias": [u"Asturias"], 
    u"Región de Murcia": [u"Murcia"], 
}

for comunidad, provincias in ccaa.items():
    de = u'de'
    if comunidad == u'Islas Baleares':
        de = u'de las'
    elif comunidad in [u'País Vasco', u'Principado de Asturias']:
        de = u'del'
    elif comunidad in [u'Comunidad Foral de Navarra', u'Comunidad de Madrid', u'Comunidad Valenciana', u'Región de Murcia']:
        de = u'de la'
    
    """
    for por in ["altitud", "población", "superficie"]:
        wtitle = "Lista de municipios %s %s por %s" % (de, comunidad, por)
        wtext = "{{Lista de municipios por lugar|país=España|comunidad autónoma=%s|sort=%s}}" % (comunidad, por)
        page = pywikibot.Page(site, wtitle)
        if False and page.exists():
            print("La pagina %s ya existe" % (wtitle))
        else:
            page.text = wtext
            page.save("BOT - Creando lista de comunidad autónoma", botflag=True)
        
        if len(provincias) > 1:
            for provincia in provincias:
                wtitle = "Lista de municipios de la provincia de %s por %s" % (provincia, por)
                wtext = "{{Lista de municipios por lugar|país=España|comunidad autónoma=%s|provincia=Provincia de %s|sort=%s}}" % (comunidad, provincia, por)
                page = pywikibot.Page(site, wtitle)
                if False and page.exists():
                    print("La pagina %s ya existe" % (wtitle))
                else:
                    page.text = wtext
                    page.save("BOT - Creando lista de provincia", botflag=True)
        else:
            wtitle = "Lista de municipios de la provincia de %s por %s" % (provincias[0], por)
            redtitle = "Lista de municipios %s %s por %s" % (de, comunidad, por)
            wtext = u"#REDIRECT [[%s]]" % (redtitle)
            page = pywikibot.Page(site, wtitle)
            if page.exists():
                print("La pagina %s ya existe" % (wtitle))
            else:
                page.text = wtext
                page.save("BOT - Creando redirect hacia [[%s]]" % (redtitle), botflag=True)
    """
    
    for por in [u"población"]:
        for year in range(2001, 2023):
            wtitle = u"Lista de municipios %s %s por %s (%s)" % (de, comunidad, por, year)
            wtext = u"{{Lista de municipios por lugar|país=España|comunidad autónoma=%s|año=%s|sort=%s}}" % (comunidad, year, por)
            page = pywikibot.Page(site, wtitle)
            if False and page.exists():
                print(u"La pagina %s ya existe" % (wtitle))
            else:
                page.text = wtext
                page.save(u"BOT - Creando lista de comunidad autónoma", botflag=True)
            
            if len(provincias) > 1:
                for provincia in provincias:
                    wtitle = u"Lista de municipios de la provincia de %s por %s (%s)" % (provincia, por, year)
                    wtext = u"{{Lista de municipios por lugar|país=España|comunidad autónoma=%s|provincia=Provincia de %s|año=%s|sort=%s}}" % (comunidad, provincia, year, por)
                    page = pywikibot.Page(site, wtitle)
                    if False and page.exists():
                        print(u"La pagina %s ya existe" % (wtitle))
                    else:
                        page.text = wtext
                        page.save(u"BOT - Creando lista de provincia", botflag=True)
            else:
                wtitle = u"Lista de municipios de la provincia de %s por %s (%s)" % (provincias[0], por, year)
                redtitle = u"Lista de municipios %s %s por %s (%s)" % (de, comunidad, por, year)
                wtext = u"#REDIRECT [[%s]]" % (redtitle)
                page = pywikibot.Page(site, wtitle)
                if page.exists():
                    print(u"La pagina %s ya existe" % (wtitle))
                else:
                    page.text = wtext
                    page.save(u"BOT - Creando redirect hacia [[%s]]" % (redtitle), botflag=True)


