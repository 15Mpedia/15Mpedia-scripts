#!/usr/bin/python
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
import urllib
import os
import re
import sys
import pywikibot

def logerror(errorline):
    error = open('crear-municipios.errores', 'a')
    error.write(errorline)
    error.close()

def removeemptyparams(text):
    return re.sub(r'(?im)^\|([^=]+)=\n\|', '|', text)

def main():
    codsccaa = {
        '01': 'Andalucía', 
        '02': 'Aragón', 
        '03': 'Principado de Asturias', 
        '04': 'Islas Baleares', 
        '05': 'Islas Canarias', 
        '06': 'Cantabria', 
        '07': 'Castilla y León', 
        '08': 'Castilla-La Mancha', 
        '09': 'Cataluña', 
        '10': 'Extremadura', 
        '11': 'Galicia', 
        '12': 'Comunidad de Madrid', 
        '13': 'Región de Murcia', 
        '14': 'Comunidad Foral de Navarra', 
        '15': 'Euskadi', 
        '16': 'La Rioja', 
        '17': 'Comunidad Valenciana', 
        '18': 'Ceuta',
        '19': 'Melilla',
        }
    codsccaaprov = {
        '01': ['04', '11', '14', '18', '21', '23', '29', '41'], #Andalucía
        '02': ['22', '44', '50'], #Aragón
        '03': ['33'], #Principado de Asturias
        '04': ['07'], #Islas Baleares
        '05': ['35', '38'], #Islas Canarias
        '06': ['39'], #Cantabria
        '07': ['05', '09', '24', '34', '37', '40', '42', '47', '49'], #Castilla y León
        '08': ['02', '13', '16', '19', '45'], #Castilla-La Mancha
        '09': ['08', '17', '25', '43'], #Cataluña
        '10': ['06', '10'], #Extremadura
        '11': ['15', '27', '32', '36'], #Galicia
        '12': ['28'], #Comunidad de Madrid
        '13': ['30'], #Región de Murcia
        '14': ['31'], #Comunidad Foral de Navarra
        '15': ['01', '20', '48'], #Euskadi
        '16': ['26'], #La Rioja
        '17': ['03', '12', '46'], #Comunidad Valenciana
        '18': ['51'], #Ceuta
        '19': ['52'], #Melilla
        }
    codsprov = {
        #Andalucía
        '04': 'Provincia de Almería', 
        '11': 'Provincia de Cádiz', 
        '14': 'Provincia de Córdoba', 
        '18': 'Provincia de Granada', 
        '21': 'Provincia de Huelva', 
        '23': 'Provincia de Jaén', 
        '29': 'Provincia de Málaga', 
        '41': 'Provincia de Sevilla', 
        #Aragón
        '22': 'Provincia de Huesca', 
        '44': 'Provincia de Teruel', 
        '50': 'Provincia de Zaragoza', 
        #Asturias
        '33': 'Provincia de Asturias', 
        #Baleares
        '07': 'Provincia de Baleares', 
        #Canarias
        '35': 'Provincia de Las Palmas', 
        '38': 'Provincia de Santa Cruz de Tenerife', 
        #Cantabria
        '39': 'Provincia de Cantabria', 
        #Castilla y León
        '05': 'Provincia de Ávila', 
        '09': 'Provincia de Burgos', 
        '24': 'Provincia de León', 
        '34': 'Provincia de Palencia', 
        '37': 'Provincia de Salamanca', 
        '40': 'Provincia de Segovia', 
        '42': 'Provincia de Soria', 
        '47': 'Provincia de Valladolid', 
        '49': 'Provincia de Zamora', 
        #Castilla-La Mancha
        '02': 'Provincia de Albacete', 
        '13': 'Provincia de Ciudad Real', 
        '16': 'Provincia de Cuenca', 
        '19': 'Provincia de Guadalajara', 
        '45': 'Provincia de Toledo', 
        #Cataluña
        '08': 'Provincia de Barcelona', 
        '17': 'Provincia de Girona', 
        '25': 'Provincia de Lleida', 
        '43': 'Provincia de Tarragona', 
        #Extremadura
        '06': 'Provincia de Badajoz', 
        '10': 'Provincia de Cáceres', 
        #Galicia
        '15': 'Provincia de A Coruña', 
        '27': 'Provincia de Lugo', 
        '32': 'Provincia de Ourense', 
        '36': 'Provincia de Pontevedra', 
        #Comunidad de Madrid
        '28': 'Provincia de Madrid', 
        #Región de Murcia
        '30': 'Provincia de Murcia', 
        #Comunidad Foral de Navarra
        '31': 'Provincia de Navarra', 
        #Euskadi
        '01': 'Provincia de Araba', 
        '20': 'Provincia de Gipuzkoa', 
        '48': 'Provincia de Bizkaia', 
        #La Rioja
        '26': 'Provincia de La Rioja', 
        #Comunidad Valenciana
        '03': 'Provincia de Alicante', 
        '12': 'Provincia de Castellón', 
        '46': 'Provincia de Valencia', 
        #Ceuta y Melilla
        '51': 'Ceuta',
        '52': 'Melilla',
        }
    
    skip = ''
    if len(sys.argv) > 1:
        skip = sys.argv[1]
    
    """
    SELECT DISTINCT ?item ?itemLabel ?ineid ?iwes
    WHERE {
      ?item wdt:P31/wdt:P279* wd:Q2074737.
      ?item wdt:P772 ?ineid.
      ?iwes schema:about ?item.
      ?iwes schema:isPartOf <https://es.wikipedia.org/>.
      SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
    }
    """
    csvfile = open('municipios-espana3.csv', 'r')
    munis = csv.reader(csvfile, delimiter=',', quotechar='"')
    
    pais = 'España'
    c = 0
    for row in munis:
        if c == 0:
            c += 1
            continue
        
        if skip:
            if row[1] != skip:
                continue
            else:
                skip = ''
        
        q = row[0].split('/entity/')[1]
        codprov = row[2][:2]
        provincia = codsprov[codprov]
        codccaa = ''
        for x, y in codsccaaprov.items():
            if codprov in y:
                codccaa = x
                break
        ccaa = codsccaa[codccaa]
        codmuni = row[2][2:]
        municipio = row[1]
        iwes = re.sub('_', ' ', urllib.parse.unquote(row[3].split('/wiki/')[1]))
        
        nombre = municipio
        print('\n', '#'*40, '\n', nombre, '\n', '#'*40, '\n')
        
        #coger info de wikipedia
        eswikititle = iwes
        eswiki = pywikibot.Page(pywikibot.Site('es', 'wikipedia'), eswikititle)
        print(eswiki)
        if eswiki.exists() and eswiki.isRedirectPage():
            eswiki = eswiki.getRedirectTarget()
            eswikititle = eswiki.title()
        
        if not eswiki.exists() or \
            (eswiki.exists() and eswiki.isDisambig()) or \
            (eswiki.exists() and not re.search(r'(?im)\{\{\s*(Ficha de localidad de España|Ficha de entidad subnacional)', eswiki.text)):
            print('Municipio %s no encontrado en eswiki. Escribiendo al log de errores' % eswikititle)
            logerror('%s no encontrado en eswiki\n' % (eswikititle))
            continue

        if eswiki.exists() and not eswiki.isRedirectPage() and not eswiki.isDisambig():
            if re.search(r'(?im)\{\{\s*(Ficha de localidad de España|Ficha de entidad subnacional)', eswiki.text):
                escudo = ''
                if re.search(r'(?im)escudo\s*=\s*.', eswiki.text):
                    try:
                        escudo = re.findall(r'(?im)escudo\s*=\s*([^\n\r\|\[\]\{\}/<]+)', eswiki.text)[0].strip()
                    except:
                        pass
                    if escudo == 'no' or not re.search(r'(?im)\.(jpe?g|pne?g|svg)', escudo):
                        escudo = ''
                bandera = ''
                if re.search(r'(?im)bandera\s*=\s*.', eswiki.text):
                    try:
                        bandera = re.findall(r'(?im)bandera\s*=\s*([^\n\r\|\[\]\{\}/<]+)', eswiki.text)[0].strip()
                    except:
                        pass
                    if bandera == 'no' or not re.search(r'(?im)\.(jpe?g|pne?g|svg)', bandera):
                        bandera = ''
                comarca = ''
                if re.search(r'(?im)comarca\s*=\s*\[\[', eswiki.text):
                    comarca = re.findall(r'(?im)comarca\s*=\s*\[\[([^\n\r\|\[\]]+?)(?:\|[^\n\r\[\]]+?)?\]\]', eswiki.text)[0].strip()
                web = ''
                if re.search(r'(?im)(?:página web|web)\s*=\s*\[?(?:https?://)?w', eswiki.text):
                    web = re.findall(r'(?im)(?:página web|web)\s*=\s*\[?((?:https?://)?w[^\s\]\<\|]+)', eswiki.text)[0].strip()
                    if web.startswith('www'):
                        web = 'http://' + web
            else:
                print('Municipio no encontrado en eswiki')
                continue
        else:
            print('Municipio no encontrado en eswiki')
            continue
        eswiki = '' #reset 
        
        infobox = """{{Infobox Municipio
|nombre=%s
|país=%s
|comunidad autónoma=%s
|comunidad autónoma código=%s
|provincia=%s
|provincia código=%s
|comarca=%s
|municipio código=%s
|escudo=%s
|bandera=%s
|sitio web=%s
|enlaces externos=* {{wikipedia|es|%s}}%s
}}""" % (nombre, pais, codsccaa[codccaa], codccaa, codsprov[codprov], codprov, comarca, codmuni, escudo, bandera, web, eswikititle, q and '\n* {{wikidata|%s}}' % (q) or '')
        infobox = removeemptyparams(infobox)
        
        page = pywikibot.Page(pywikibot.Site('15mpedia', '15mpedia'), '%s' % (nombre))
        if page.exists() and page.isRedirectPage():
            page = page.getRedirectTarget()
        
        if page.exists():
            if not re.search(r'(?im)\{\{\s*Infobox Municipio', page.text):
                print('La pagina existe pero no tiene infobox municipio')
                logerror('%s existe en 15Mpedia pero no tiene infobox\n\n%s\n\n' % (nombre, infobox))
                continue
            
            if not re.search(r'(?im)municipio código=%s' % (codmuni), page.text):
                print('La pagina existe pero el código de municipio %s no coincide' % (codmuni))
                logerror('%s existe en 15Mpedia pero el código de municipio %s no coincide\n\n%s\n\n' % (nombre, codmuni, infobox))
                continue
            
            print('La pagina ya existe, rellenando lo que falta')
            newtext = page.text
            newtext = removeemptyparams(newtext)
            add = []
            if not re.search(r'(?im)\|nombre=', newtext) and nombre:
                add.append('|nombre=%s' % (nombre))
            if not re.search(r'(?im)\|país=', newtext) and pais:
                add.append('|país=%s' % (pais))
            if not re.search(r'(?im)\|comunidad autónoma=', newtext) and codsccaa[codccaa]:
                add.append('|comunidad autónoma=%s' % (codsccaa[codccaa]))
            if not re.search(r'(?im)\|comunidad autónoma código=', newtext) and codccaa:
                add.append('|comunidad autónoma código=%s' % (codccaa))
            if not re.search(r'(?im)\|provincia=', newtext) and codsprov[codprov]:
                add.append('|provincia=%s' % (codsprov[codprov]))
            if not re.search(r'(?im)\|provincia código=', newtext) and codprov:
                add.append('|provincia código=%s' % (codprov))
            if not re.search(r'(?im)\|comarca=', newtext) and comarca:
                add.append('|comarca=%s' % (comarca))
            if not re.search(r'(?im)\|municipio código=', newtext) and codmuni:
                add.append('|municipio código=%s' % (codmuni))
            if not re.search(r'(?im)\|escudo=', newtext) and escudo:
                add.append('|escudo=%s' % (escudo))
            if not re.search(r'(?im)\|bandera=', newtext) and bandera:
                add.append('|bandera=%s' % (bandera))
            #if not re.search(r'(?im)\|deuda viva=', newtext) and deuda2010:
            #    add.append('|deuda viva={{deuda viva|año=2010|euros=%s}}' % (deuda2010))
            if not re.search(r'(?im)\|sitio web=', newtext) and web:
                add.append('|sitio web=%s' % (web))
            if not re.search(r'(?im)\|enlaces externos=', newtext):
                if eswikititle:
                    add.append('|enlaces externos=* {{wikipedia|es|%s}}\n{{wikidata|%s}}' % (eswikititle, q))
            elif re.search(r'(?im)\{\{wikipedia\|es\|%s\}\}' % (eswikititle), newtext) and not re.search(r'(?im)\{\{wikidata', newtext):
                newtext = re.sub(r'(?im)(\{\{wikipedia\|es\|%s\}\})' % (eswikititle), r'\1\n{{wikidata|%s}}' % (q), newtext)
            
            if add or newtext != page.text:
                if add:
                    newtext = newtext.replace('{{Infobox Municipio', '{{Infobox Municipio\n%s' % ('\n'.join(add)))
                    newtext = removeemptyparams(newtext)
                if page.text != newtext and len(newtext) > len(page.text):
                    pywikibot.showDiff(page.text, newtext)
                    page.text = newtext
                    page.save('BOT - Añadiendo datos de Wikipedia', botflag=True)
            else:
                print('Nada que añadir')
        else:
            print(infobox)
            page.text = infobox
            page.save('BOT - Creando municipio usando Wikipedia', botflag=False)
        
        c += 1

if __name__ == '__main__':
    main()
