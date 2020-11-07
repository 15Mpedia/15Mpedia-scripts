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

paises = [
    "Alemania", 
    "Angola", 
    "Argelia", 
    "Australia", 
    "Bélgica", 
    "Bolivia", 
    "Brasil", 
    "Canadá", 
    "Chile", 
    "China", 
    "Colombia", 
    "Cuba", 
    "Ecuador", 
    "El Salvador", 
    "España", 
    "Estados Unidos", 
    "Finlandia", 
    "Francia", 
    "Grecia", 
    "Honduras", 
    "Irán", 
    "Italia", 
    "Japón", 
    "Marruecos", 
    "México", 
    "Nicaragua", 
    "Noruega", 
    "Panamá", 
    "Paraguay", 
    "Países Bajos", 
    "Perú", 
    "Polonia", 
    "Portugal", 
    "Reino Unido", 
    "Rusia", 
    "Suecia", 
    "Turquía", 
    "Ucrania", 
    "Uruguay", 
    "Venezuela", 
    "Vietnam", 
]
paisesminimum = [
    "Alemania", 
    "Bélgica", 
    "Bolivia", 
    "Brasil", 
    "Canadá", 
    "Chile", 
    "China", 
    "Colombia", 
    "Cuba", 
    "Ecuador", 
    "El Salvador", 
    "España", 
    "Estados Unidos", 
    "Finlandia", 
    "Francia", 
    "Grecia", 
    "Honduras", 
    "Italia", 
    "Marruecos", 
    "México", 
    "Nicaragua", 
    "Noruega", 
    "Panamá", 
    "Paraguay", 
    "Países Bajos", 
    "Perú", 
    "Polonia", 
    "Portugal", 
    "Reino Unido", 
    "Rusia", 
    "Suecia", 
    "Turquía", 
    "Ucrania", 
    "Uruguay", 
    "Venezuela", 
]
overwrite = True
site = pywikibot.Site('15mpedia', '15mpedia')
for pais in paisesminimum:
    """title = 'Cine de %s' % (pais)
    p = pywikibot.Page(site, title)
    if not p.exists():
        output = "{{Cine por lugar|país=%s}}" % (pais)
        p.text = output
        p.save("BOT - Creando página")
    title = 'Cine en %s' % (pais)
    p = pywikibot.Page(site, title)
    if not p.exists():
        output = "#redirect [[Cine de %s]]" % (pais)
        p.text = output
        p.save("BOT - Creando redirect")
    
    title = 'Lista de películas de %s' % (pais)
    p = pywikibot.Page(site, title)
    if not p.exists():
        output = "{{Lista de películas por lugar|país=%s}}" % (pais)
        p.text = output
        p.save("BOT - Creando lista")
    
    title = 'Lista de documentales de %s' % (pais)
    p = pywikibot.Page(site, title)
    if not p.exists():
        output = "{{Lista de documentales por lugar|país=%s}}" % (pais)
        p.text = output
        p.save("BOT - Creando lista")
    """
    temas = [
        "Lista de asambleas", 
        "Lista de asociaciones", 
        "Lista de bancos de tiempo", 
        "Lista de centros sociales", 
        "Lista de comedores sociales", 
        "Lista de cooperativas", 
        "Lista de plataformas", 
        "Lista de colectivos", 
        "Lista de manifestaciones", 
        "Lista de actividades", 
        "Lista de acampadas", 
        "Lista de acontecimientos", 
    ]
    for tema in temas:
        title = '%s de %s' % (tema, pais)
        p = pywikibot.Page(site, title)
        if overwrite or not p.exists():
            output = "{{%s por lugar|país=%s}}" % (tema, pais)
            p.text = output
            p.save("BOT - Creando lista")
        
        title = '%s en %s' % (tema, pais)
        p = pywikibot.Page(site, title)
        if overwrite or not p.exists():
            output = "#redirect [[%s de %s]]" % (tema, pais)
            p.text = output
            p.save("BOT - Creando redirect")
