#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2020 emijrp <emijrp@gmail.com>
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

def createredirect(title='', target='', overwrite=False, botflag=True):
    pagered = pywikibot.Page(site, title)
    wtextred = '#REDIRECT [[%s]]' % (target)
    if not overwrite and pagered.exists():
        print("La redirect %s ya existe" % (title))
    else:
        pagered.text = wtextred
        pagered.save("BOT - Creando redirect", botflag=botflag)

site = pywikibot.Site('15mpedia', '15mpedia')
ccaa = {
    "Andalucía": ["Almería", "Cádiz", "Córdoba", "Granada", "Huelva", "Jaén", "Málaga", "Sevilla"], 
    "Aragón": ["Huesca", "Teruel", "Zaragoza"], 
    "Canarias": ["Las Palmas", "Santa Cruz de Tenerife"], 
    "Cantabria": ["Cantabria"], 
    "Castilla-La Mancha": ["Albacete", "Ciudad Real", "Cuenca", "Guadalajara", "Toledo"], 
    "Castilla y León": ["Ávila", "Burgos", "León", "Palencia", "Salamanca", "Segovia", "Soria", "Valladolid", "Zamora"], 
    "Cataluña": ["Barcelona", "Girona", "Lleida", "Tarragona"], 
    "Comunidad de Madrid": ["Madrid"], 
    "Comunidad Foral de Navarra": ["Navarra"], 
    "Comunidad Valenciana": ["Alicante", "Castellón", "Valencia"], 
    "Extremadura": ["Badajoz", "Cáceres"], 
    "Galicia": ["A Coruña", "Lugo", "Ourense", "Pontevedra"], 
    "Islas Baleares": ["Baleares"], 
    "La Rioja": ["La Rioja"], 
    "País Vasco": ["Álava", "Gipuzkoa", "Vizcaya"], 
    "Principado de Asturias": ["Asturias"], 
    "Región de Murcia": ["Murcia"], 
}

preposicion = 'de' #de o en
preposicion_redirect = 'en' #de o en o vacio
overwrite = False #True or False
botflag = True #True or False

temas = [
    "Movimiento 15M", 
    "Lista de bancos de tiempo", 
    "Lista de centros sociales", 
    "Lista de comedores sociales", 
    "Lista de cooperativas", 
    "Lista de plataformas", 
    "Lista de realojos", 
    "Lista de colectivos", 
    "Lista de manifestaciones", 
    "Lista de acampadas", 
    "Lista de actividades", 
    "Lista de acontecimientos", 
]

for tema in temas:
    for comunidad, provincias in ccaa.items():
        prep = preposicion
        prep_red = preposicion_redirect
        if comunidad == 'Islas Baleares':
            if preposicion == 'de':
                prep = 'de las'
            elif preposicion == 'en':
                prep = 'en las'
            if prep_red == 'de':
                prep_red = 'de las'
            elif prep_red == 'en':
                prep_red = 'en las'
        elif comunidad in ['País Vasco', 'Principado de Asturias']:
            if preposicion == 'de':
                prep = 'del'
            elif preposicion == 'en':
                prep = 'en el'
            if prep_red == 'de':
                prep_red = 'del'
            elif prep_red == 'en':
                prep_red = 'en el'
        elif comunidad in ['Comunidad Foral de Navarra', 'Comunidad de Madrid', 'Comunidad Valenciana', 'Región de Murcia']:
            if preposicion == 'de':
                prep = 'de la'
            elif preposicion == 'en':
                prep = 'en la'
            if prep_red == 'de':
                prep_red = 'de la'
            elif prep_red == 'en':
                prep_red = 'en la'
        
        wtitle = "%s %s %s" % (tema, prep, comunidad)
        wtext = "{{%s por lugar|país=España|comunidad autónoma=%s}}" % (tema, comunidad)
        page = pywikibot.Page(site, wtitle)
        if not overwrite and page.exists():
            print("La pagina %s ya existe" % (wtitle))
        else:
            page.text = wtext
            page.save("BOT - Creando página por comunidad autónoma", botflag=botflag)
        
        if prep_red:
            titlered = "%s %s %s" % (tema, prep_red, comunidad)
            targetred = "%s %s %s" % (tema, prep, comunidad)
            createredirect(title=titlered, target=targetred, overwrite=overwrite, botflag=botflag)
        
        if len(provincias) > 1:
            for provincia in provincias:
                wtitle = "%s %s la provincia de %s" % (tema, preposicion, provincia)
                wtext = "{{%s por lugar|país=España|comunidad autónoma=%s|provincia=Provincia de %s}}" % (tema, comunidad, provincia)
                page = pywikibot.Page(site, wtitle)
                if not overwrite and page.exists():
                    print("La pagina %s ya existe" % (wtitle))
                else:
                    page.text = wtext
                    page.save("BOT - Creando página por provincia", botflag=botflag)
                
                if prep_red:
                    titlered = "%s %s la provincia de %s" % (tema, preposicion_redirect, provincia)
                    targetred = "%s %s la provincia de %s" % (tema, preposicion, provincia)
                    createredirect(title=titlered, target=targetred, overwrite=overwrite, botflag=botflag)
        else:
            wtitle = "%s %s la provincia de %s" % (tema, preposicion, provincias[0])
            redtitle = "%s %s %s" % (tema, prep, comunidad)
            wtext = u"#REDIRECT [[%s]]" % (redtitle)
            page = pywikibot.Page(site, wtitle)
            if not overwrite and page.exists():
                print("La pagina %s ya existe" % (wtitle))
            else:
                page.text = wtext
                page.save("BOT - Creando redirect hacia [[%s]]" % (redtitle), botflag=botflag)
            
            if prep_red:
                titlered = "%s %s la provincia de %s" % (tema, preposicion_redirect, provincias[0])
                targetred = "%s %s la provincia de %s" % (tema, preposicion, provincias[0])
                createredirect(title=titlered, target=targetred, overwrite=overwrite, botflag=botflag)
