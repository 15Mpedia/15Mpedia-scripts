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

import csv
import json
import pywikibot
import pywikibot.pagegenerators as pagegenerators
import re
import time
import sys

def logerror(errorline):
    error = open('superficie-municipios.errores', 'a')
    error.write(errorline)
    error.close()

def main():
    site = pywikibot.Site('15mpedia', '15mpedia')
    catnames = [
        'Categoría:Municipios de España', 
    ]
    start = ''
    skip = ''
    if len(sys.argv) > 1:
        skip = sys.argv[1]
        start = sys.argv[1]
    
    csvfile = open('municipios.csv', 'r')
    muniscsv = csv.reader(csvfile, delimiter=',', quotechar='"')
    municipios = []
    c = 0
    for row in muniscsv:
        #CODIGO_CA,COMUNIDAD_AUTONOMA,Codigo Provincia,PROVINCIA,NUMERO_INSCRIPCION,Codigo Municipio,DENOMINACION,FECHA_INSCRIPCION,SUPERFICIE,HABITANTES,DENSIDAD,CAPITALIDAD
        #1,Andalucía,13391,Málaga,1290712,9762,Moclinejo,15/09/86,"14,37",1271,"88,45",Moclinejo
        if c == 0:
            c += 1
            continue
        #el codigo municipio esta dentro de 1290712, 1 ignorar, 29 prov, 071 = codigo ine, 2 no se
        municod = row[4][3:6]
        muniprovcod = row[4][1:3]
        muninombre = row[6]
        muninombre = ', ' in muninombre and muninombre.split(', ')[1]+' '+muninombre.split(', ')[0] or muninombre
        muninombre = muninombre.startswith("L' ") and muninombre.replace("L' ", "L'") or muninombre
        munisup = row[8]
        if munisup.startswith(','):
            munisup = '0'+munisup
        municipios.append([municod, muniprovcod, muninombre, munisup])
        #print(municod, muniprovcod, muninombre, munisup)
        c += 1
    
    for catname in catnames:
        category = pywikibot.Category(site, catname)
        gen = pagegenerators.CategorizedPageGenerator(category=category, start=start, namespaces=[0])
        pre = pagegenerators.PreloadingGenerator(gen, pageNumber=50)
        
        for page in pre:
            if not page.exists() or page.isRedirectPage():
                continue
            wtext = page.text
            wtitle = page.title()
            
            if skip:
                if skip == wtitle:
                    skip = ''
                else:
                    print("Skiping", wtitle)
                    continue
            
            print('\n== %s ==' % (wtitle))
            if not re.search(r'{{Infobox Municipio', wtext):
                print("No tiene infobox municipio")
                continue
            
            nombre = re.findall(r"(?m)\|nombre=([^\n\|]+)", wtext)
            nombre = nombre and nombre[0] or ''
            provcod = re.findall(r"(?m)\|provincia código=([^\n\|]+)", wtext)
            provcod = provcod and provcod[0] or ''
            cod = re.findall(r"(?m)\|municipio código=([^\n\|]+)", wtext)
            cod = cod and cod[0] or ''
            sup = re.findall(r"(?m)\|superficie=([^\n\|]+)", wtext)
            sup = sup and sup[0] or ''
            if nombre and provcod and cod:
                newtext = wtext
                found = False
                for municod, muniprovcod, muninombre, munisup in municipios:
                    if provcod == muniprovcod and cod == municod:#(nombre == muninombre or nombre in muninombre.split('/')):
                        found = True
                        print(sup, munisup)
                        newtext = re.sub(r'(?m)(\|superficie=[\d\.\,]+)', '|superficie=%s' % (munisup), newtext)
                        if not re.search(r'(?m)\|superficie=', newtext):
                            newtext = newtext.replace("{{Infobox Municipio", """{{Infobox Municipio\n|superficie=%s""" % (munisup))
                        if wtext != newtext:
                            pywikibot.showDiff(wtext, newtext)
                            page.text = newtext
                            page.save("BOT - Añadiendo dato de superficie", botflag=True)
                        if sup and munisup:
                            if float(sup.replace(',', '.')) > float(munisup.replace(',', '.'))*2 or float(sup.replace(',', '.'))*2 < float(munisup.replace(',', '.')):
                                msg = '[[%s]] tenia superficie con mucha diferencia\n' % (wtitle)
                                print(msg)
                                logerror(msg)
                        
                        #nombre oficial
                        wtext = page.text
                        newtext = wtext
                        if not re.search(r'(?m)\|nombre oficial=', newtext):
                            newtext = newtext.replace("{{Infobox Municipio", """{{Infobox Municipio\n|nombre oficial=%s""" % (muninombre))
                            pywikibot.showDiff(wtext, newtext)
                            page.text = newtext
                            page.save("BOT - Añadiendo nombre oficial %s" % (muninombre), botflag=True)
                        
                        #crea redirect
                        if nombre != muninombre and wtitle != muninombre:
                            redtext = "#redirect [[%s]]" % (wtitle)
                            redpage = pywikibot.Page(site, muninombre)
                            if not redpage.exists():
                                redpage.text = redtext
                                redpage.save("BOT - Creando redirect hacia [[%s]]" % (wtitle), botflag=True)
                        
                        break
                if not found:
                    msg = '[[%s]] no se encontro en el csv\n' % (wtitle)
                    print(msg)
                    logerror(msg)

if __name__ == '__main__':
    main()
      
