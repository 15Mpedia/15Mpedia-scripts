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

temas = [
    "15M", 
    "Agua", 
    "Alimentación", 
    "Anarquismo", 
    "Anticapitalismo", 
    "Antifascismo", 
    "Antimilitarismo", 
    "Antirepresión", 
    "Apoyo mutuo", 
    "Arte", 
    "Autogestión", 
    "Capitalismo", 
    "Censura", 
    "Ciencia", 
    "Comunicación", 
    "Comunismo", 
    "Consumo", 
    "Corrupción", 
    "Cultura", 
    "Cultura libre", 
    "Democracia", 
    "Derechos de los animales", 
    "Desobediencia civil", 
    "Ecología", 
    "Economía", 
    "Educación", 
    "Energía", 
    "Feminismo", 
    "Guerra", 
    "Historia", 
    "Imperialismo", 
    "Información", 
    "Internet", 
    "Intervención social", 
    "Justicia", 
    "LGBT", 
    "Mapas", 
    "Medio ambiente", 
    "Memoria histórica", 
    "Migración", 
    "Movimientos sociales", 
    "Okupación", 
    "Periodismo", 
    "Psicología", 
    "Política", 
    "Publicidad", 
    "Religión", 
    "Represión", 
    "Revoluciones", 
    "Sanidad", 
    "Servicios públicos", 
    "Sindicalismo", 
    "Software libre", 
    "Tercera edad", 
    "Trabajo", 
    "Transparencia", 
    "Transporte", 
    "Turismo", 
    "Urbanismo", 
    "Vivienda", 
]
temascaps = [ #mayusculas casos especiales
    "15M", 
    "Internet", 
    "LGBT", 
]
site = pywikibot.Site('15mpedia', '15mpedia')
for tema in temas:
    tema_ = tema
    if not tema_ in temascaps:
        tema_ = tema_.lower()
    
    title = 'Lista de obras sobre %s' % (tema_)
    p = pywikibot.Page(site, title)
    if not p.exists():
        output = "{{Lista de obras por tema|tema=%s}}" % (tema)
        p.text = output
        p.save("BOT - Creando lista")
    
    title = 'Lista de obras de %s' % (tema_)
    p = pywikibot.Page(site, title)
    if not p.exists():
        output = "#redirect [[Lista de obras sobre %s]]" % (tema_)
        p.text = output
        p.save("BOT - Creando redirect")
    
    cats = [
        ["Obras", "obras"], 
        ["Documentales", "documentales"], 
        ["Libros", "libros"], 
        ["Películas", "películas"], 
    ]
    for x, y in cats:
        title = 'Categoría:%s sobre %s' % (x, tema_)
        p = pywikibot.Page(site, title)
        if not p.exists():
            output = "{{Categoría %s por tema|tema=%s}}" % (y, tema)
            p.text = output
            p.save("BOT - Creando categoría")
    
    title = 'Literatura sobre %s' % (tema_)
    p = pywikibot.Page(site, title)
    if not p.exists():
        output = "{{Literatura por tema|tema=%s}}" % (tema)
        p.text = output
        p.save("BOT - Creando página")
    
    #literatura y libros
    title = 'Literatura de %s' % (tema_)
    p = pywikibot.Page(site, title)
    if not p.exists():
        output = "#redirect [[Literatura sobre %s]]" % (tema_)
        p.text = output
        p.save("BOT - Creando redirect")
    
    title = 'Lista de libros sobre %s' % (tema_)
    p = pywikibot.Page(site, title)
    if not p.exists():
        output = "{{Lista de libros por tema|tema=%s}}" % (tema)
        p.text = output
        p.save("BOT - Creando lista")
    
    title = 'Lista de libros de %s' % (tema_)
    p = pywikibot.Page(site, title)
    if not p.exists():
        output = "#redirect [[Lista de libros sobre %s]]" % (tema_)
        p.text = output
        p.save("BOT - Creando redirect")
    
    #cine y peliculas
    title = 'Cine sobre %s' % (tema_)
    p = pywikibot.Page(site, title)
    if not p.exists():
        output = "{{Cine por tema|tema=%s}}" % (tema)
        p.text = output
        p.save("BOT - Creando página")
    
    title = 'Cine de %s' % (tema_)
    p = pywikibot.Page(site, title)
    if not p.exists():
        output = "#redirect [[Cine sobre %s]]" % (tema_)
        p.text = output
        p.save("BOT - Creando redirect")
    
    title = 'Lista de películas sobre %s' % (tema_)
    p = pywikibot.Page(site, title)
    if not p.exists():
        output = "{{Lista de películas por tema|tema=%s}}" % (tema)
        p.text = output
        p.save("BOT - Creando lista")
    
    title = 'Lista de películas de %s' % (tema_)
    p = pywikibot.Page(site, title)
    if not p.exists():
        output = "#redirect [[Lista de películas sobre %s]]" % (tema_)
        p.text = output
        p.save("BOT - Creando redirect")
    
    title = 'Lista de documentales sobre %s' % (tema_)
    p = pywikibot.Page(site, title)
    if not p.exists():
        output = "{{Lista de documentales por tema|tema=%s}}" % (tema)
        p.text = output
        p.save("BOT - Creando lista")
    
    title = 'Lista de documentales de %s' % (tema_)
    p = pywikibot.Page(site, title)
    if not p.exists():
        output = "#redirect [[Lista de documentales sobre %s]]" % (tema_)
        p.text = output
        p.save("BOT - Creando redirect")
    
