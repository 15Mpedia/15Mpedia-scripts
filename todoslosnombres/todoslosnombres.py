#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2018 emijrp <emijrp@gmail.com>
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

import re
import time
import urllib.parse
import urllib.request
import pywikibot
import pywikibot.pagegenerators as pagegenerators

def invertirfecha(fecha):
    if len(fecha.split('/')) == 3:
        fecha = '%s/%s/%s' % (fecha.split('/')[2], fecha.split('/')[1], fecha.split('/')[0])
    return fecha

def traducirfecha(fecha):
    trad = fecha
    meses = {1:'enero', 2:'febrero', 3:'marzo', 4:'abril', 5:'mayo', 6:'junio', 7:'julio', 8:'agosto', 9:'septiembre', 10:'octubre', 11:'noviembre', 12:'diciembre'}
    if len(fecha.split('/')) == 3:
        try:
            trad = '%s de %s de %s' % (int(fecha.split('/')[2]), meses[int(fecha.split('/')[1])], fecha.split('/')[0])
        except:
            trad = fecha.split('/')[0]
    
    return trad

def archiveurl(url='', force=False):
    if url:
        #check if available in IA
        prefix = 'https://archive.org/wayback/available?url='
        checkurl = prefix + url
        raw = getURL(url=checkurl)
        #print(raw)
        if '"archived_snapshots": {}' in raw or force:
            #not available, archive it
            #print('Archiving URL',url)
            prefix2 = 'https://web.archive.org/save/'
            saveurl = prefix2 + url
            try:
                f = urllib.request.urlopen(saveurl)
                raw = f.read().decode('utf-8')
                print('Archived at https://web.archive.org/web/*/%s' % (url))
                return 'ok'
            except:
                print('Error 404 https://web.archive.org/web/*/%s' % (url))
                return '404'
        else:
            print('Previously archived at https://web.archive.org/web/*/%s' % (url))
            return 'previously'
            #print(raw)

def getURL(url=''):
    raw = ''
    req = urllib.request.Request(url, headers={ 'User-Agent': 'Mozilla/5.0' })
    try:
        raw = urllib.request.urlopen(req).read().strip().decode('utf-8')
    except:
        try:
            raw = urllib.request.urlopen(req).read().strip().decode('latin-1')
        except:
            sleep = 10 # seconds
            maxsleep = 60
            while sleep <= maxsleep:
                print('Error while retrieving: %s' % (url))
                print('Retry in %s seconds...' % (sleep))
                time.sleep(sleep)
                try:
                    raw = urllib.request.urlopen(req).read().strip().decode('utf-8')
                except:
                    pass
                sleep = sleep * 2
    return raw

def main():
    site = pywikibot.Site('15mpedia', '15mpedia')
    tlnpage = pywikibot.Page(site, "Todos los nombres/Dataset municipios")
    municipiosids = re.findall(r'id=(\d+)', tlnpage.text)
    
    f = open('nombrespilamujer', 'r')
    nombrespilamujer = f.read().lower().strip().splitlines()
    f.close()
    
    skipmuni = '8408'
    skipbio = 'lorenzo-jimenez-raya' #minusculas y espacios como -
    skippage = 144 #para municipios grandes, podemos saltar a la pagina concreta http://www.todoslosnombres.org/taxonomy/term/8408?page=144
    for municipioid in municipiosids:
        if skipmuni:
            if skipmuni == municipioid:
                skipmuni = ''
            else:
                print("Skiping", municipioid)
                continue
        url = 'http://www.todoslosnombres.org/taxonomy/term/' + municipioid
        urlsave = 'https://web.archive.org/web/2025/' + url
        d = 1
        raw = ''
        while not raw and d <= 5:
            status = archiveurl(url=url, force=True)
            try:
                raw = getURL(url=urlsave)
            except:
                print("Error, no existe pagina para el municipio?")
                continue
            time.sleep(10*d)
            d += 1
        if not raw:
            print("Error leyendo municipio, saltando")
            continue
        municipionombre = re.findall(r'(?im)id="page-title">([^<>]+?)</h1>', raw)[0]
        print('==', municipionombre, '==')
        print(url)
        
        if '/' in municipionombre or '?' in municipionombre or ',' in municipionombre or '&' in municipionombre or '.' in municipionombre:
            print("Saltando municipio ambiguo")
            continue
        
        if re.search(r'(?im)Actualmente no hay contenido', raw):
            print("Este municipio no tiene fichas")
            continue
        time.sleep(10)
        
        m = re.findall(r'(?im)page=(\d+)', raw)
        numpages = m and max([int(n) for n in m]) or 0
        c = 0
        if skippage:
            print("Skiping to page", skippage)
            c = skippage
            skippage = ''
        while c <= numpages:
            raw2 = ''
            if c != 0:
                url2 = 'http://www.todoslosnombres.org/taxonomy/term/%s?page=%s' % (municipioid, str(c))
                status = '404'
                d = 1
                while status == '404' and d <= 3:
                    status = archiveurl(url=url2, force=True)
                    d += 1
                    time.sleep((d-1)*20+10)
                if status == '404':
                    continue
                url2save = 'https://web.archive.org/web/2025/' + url2
                try:
                    raw2 = getURL(url=url2save)
                except:
                    print("Error al leer la pagina del municipio")
                    break
            else:
                raw2 = raw
            time.sleep(10)
            personas = re.findall(r'(?im)node-title"><a href="[^<>]+/content/personas/([^<>]+)">', raw2)
            if not personas:
                print("No hay mas personas en este municipio")
                break
            for persona in personas:
                print('\n==', persona, '==\n')
                if skipbio:
                    if skipbio == persona:
                        skipbio = ''
                    else:
                        print("Saltando", persona)
                        continue
                url3 = 'http://www.todoslosnombres.org/content/personas/' + persona
                
                status = '404'
                d = 1
                while status == '404' and d <= 3:
                    status = archiveurl(url=url3, force=True)
                    d += 1
                    time.sleep((d-1)*20+10)
                if status == '404':
                    print("Error al leer la ficha")
                    continue
                url3save = 'https://web.archive.org/web/2025/' + url3
                try:
                    raw3 = getURL(url=url3save)
                except:
                    print("Error al leer la ficha")
                    continue
                
                apellido1 = ''
                apellido1regexp = r'(?im)Primer apellido[^<>]+?</div><div class="field-items"><div class="field-item even">([^<>]+?)</div>'
                if re.search(apellido1regexp, raw3):
                    apellido1 = re.findall(apellido1regexp, raw3)[0].strip()
                apellido2 = ''
                apellido2regexp = r'(?im)Segundo apellido[^<>]+?</div><div class="field-items"><div class="field-item even">([^<>]+?)</div>'
                if re.search(apellido2regexp, raw3):
                    apellido2 = re.findall(apellido2regexp, raw3)[0].strip()
                nombrepila = ''
                nombreregexp = r'(?im)Nombre[^<>]+?</div><div class="field-items"><div class="field-item even">([^<>]+?)</div>'
                if re.search(nombreregexp, raw3):
                    nombrepila = re.findall(nombreregexp, raw3)[0].strip()
                
                if nombrepila and apellido1 and apellido2:
                    nombrecompleto = nombrepila + ' ' + apellido1 + ' ' + apellido2
                    nombrecompleto2 = apellido1 + ' ' + apellido2 + ', ' + nombrepila
                    print(nombrecompleto)
                else:
                    print("Falta nombre o apellidos")
                    continue
                
                if '/' in nombrecompleto:
                    print("Nombre ambiguo")
                    continue
                
                apodo = ''
                apodoregexp = r'(?im)Apodo:&nbsp;</div><div class="field-items"><div class="field-item even">([^<>]+?)</div>'
                if re.search(apodoregexp, raw3):
                    apodo = re.findall(apodoregexp, raw3)[0].strip()
                
                sexo = 'Hombre'
                if nombrepila.lower() in nombrespilamujer:
                    sexo = 'Mujer'
                
                prof = ''
                profregexp = r'(?im)Profesión[^<>]+?</div><div class="field-items"><div class="field-item even">([^<>]+?)</div>'
                if re.search(profregexp, raw3):
                    prof = re.findall(profregexp, raw3)[0].strip()
                
                if prof.lower() == 'labores':
                    prof = 'ama de casa'
                if prof.lower() == 'campo':
                    prof = 'trabajador del campo'
                    if sexo == 'Mujer':
                        prof = 'trabajadora del campo'
                
                lugnacimiento = ''
                lugnacimientoregexp = r'(?im)Municipio de nacimiento[^<>]+?</div><div class="field-items"><div class="field-item even">([^<>]+?)</div>'
                if re.search(lugnacimientoregexp, raw3):
                    lugnacimiento = re.findall(lugnacimientoregexp, raw3)[0].strip()
                if not lugnacimiento: #probamos con la provincia
                    lugnacimientoregexp = r'(?im)Provincia de nacimiento[^<>]+?</div><div class="field-items"><div class="field-item even">([^<>]+?)</div>'
                    if re.search(lugnacimientoregexp, raw3):
                        lugnacimiento = re.findall(lugnacimientoregexp, raw3)[0].strip()
                        if not 'provincia' in lugnacimiento.lower():
                            lugnacimiento = 'Provincia de ' + lugnacimiento
                
                lugresidencia = ''
                lugresidenciaregexp = r'(?im)Municipio de residencia[^<>]+?</div><div class="field-items"><div class="field-item even">([^<>]+?)</div>'
                if re.search(lugresidenciaregexp, raw3):
                    lugresidencia = re.findall(lugresidenciaregexp, raw3)[0].strip()
                if not lugresidencia: #probamos con la provincia
                    lugresidenciaregexp = r'(?im)Provincia de residencia[^<>]+?</div><div class="field-items"><div class="field-item even">([^<>]+?)</div>'
                    if re.search(lugresidenciaregexp, raw3):
                        lugresidencia = re.findall(lugresidenciaregexp, raw3)[0].strip()
                        if not 'provincia' in lugresidencia.lower():
                            lugresidencia = 'Provincia de ' + lugresidencia
                
                lugfallecimiento = ''
                lugfallecimientoregexp = r'(?im)Lugar fallecimiento[^<>]+?</div><div class="field-items"><div class="field-item even">([^<>]+?)</div>'
                if re.search(lugfallecimientoregexp, raw3):
                    lugfallecimiento = re.findall(lugfallecimientoregexp, raw3)[0].strip()
                if not lugfallecimiento: #probamos con la provincia
                    lugfallecimientoregexp = r'(?im)Provincia fallecimiento[^<>]+?</div><div class="field-items"><div class="field-item even">([^<>]+?)</div>'
                    if re.search(lugfallecimientoregexp, raw3):
                        lugfallecimiento = re.findall(lugfallecimientoregexp, raw3)[0].strip()
                        if not 'provincia' in lugfallecimiento.lower():
                            lugfallecimiento = 'Provincia de ' + lugfallecimiento
                
                fechanacimiento = ''
                fechanacimientoregexp = r'(?im)Fecha nacimiento[^<>]+?</div><div class="field-items"><div class="field-item even">([^<>]+?)</div>'
                if re.search(fechanacimientoregexp, raw3):
                    fechanacimiento = re.findall(fechanacimientoregexp, raw3)[0].strip()
                
                fechafallecimiento = ''
                fechafallecimientoregexp = r'(?im)Fecha fallecimiento[^<>]+?</div><div class="field-items"><div class="field-item even">([^<>]+?)</div>'
                if re.search(fechafallecimientoregexp, raw3):
                    fechafallecimiento = re.findall(fechafallecimientoregexp, raw3)[0].strip()
                
                causafallecimiento = ''
                causafallecimientoregexp = r'(?im)Causa fallecimiento[^<>]+?</div><div class="field-items"><div class="field-item even">([^<>]+?)</div>'
                if re.search(causafallecimientoregexp, raw3):
                    causafallecimiento = re.findall(causafallecimientoregexp, raw3)[0].strip()
                
                if re.search(r'(?im)(fusilad[oa]|fusilamiento)', causafallecimiento):
                    print('Fusilado', url3)
                else:
                    print("No fue fusilado, saltamos")
                    continue
                
                bio = ''
                if lugnacimiento:
                    if 'provincia' in lugnacimiento.lower():
                        bio += '%s nació en la [[%s]].' % (nombrepila, lugnacimiento.replace("Provincia", "provincia"))
                    else:
                        bio += '%s nació en [[%s]].' % (nombrepila, lugnacimiento)
                if prof:
                     if bio:
                         bio += ' Era %s.' % (prof.lower())
                     else:
                         bio += '%s era %s.' % (nombrepila, prof.lower())
                
                if bio:
                    bio += '<ref name="todoslosnombres" />'
                
                if fechanacimiento and (len(re.findall('/', fechafallecimiento)) != 2 or len(fechafallecimiento) != 10):
                    fechanacimiento = '' #blanqueamos, incompleta
                
                if not fechafallecimiento or len(re.findall('/', fechafallecimiento)) != 2 or len(fechafallecimiento) != 10:
                    print("Fecha fallecimiento incompleta, saltamos")
                    continue
                
                desc = '%s por el franquismo, %s el %s.' % (sexo=='Hombre' and 'Represaliado' or 'Represaliada', sexo=='Hombre' and 'fusilado' or 'fusilada', traducirfecha(invertirfecha(fechafallecimiento)))
                
                output = """{{Infobox Persona
|nombre=%s
|primer apellido=%s
|segundo apellido=%s
|apodo=%s
|sexo=%s
|lugar de nacimiento=%s
|fecha de nacimiento=%s
|lugar de fallecimiento=%s
|fecha de fallecimiento=%s
|lugar de residencia=%s
|ocupación=%s
|descripción=%s
|represión={{persona represaliada
|represión=Fusilamiento
|represor=Franquismo
|fecha=%s
|lugar=%s
}}
}}
'''%s''', %s por el [[franquismo]], [[Lista de personas fusiladas por el franquismo|%s]] el [[%s]].<ref name="todoslosnombres">{{todos los nombres}}</ref>

== Biografía ==

%s

== Véase también ==
* [[Memoria histórica]]
* [[Represión franquista]]
* [[Lista de personas fusiladas por el franquismo]]

== Referencias ==
{{reflist}}

== Enlaces externos ==
{{enlaces externos}}
* {{todos los nombres|%s}}
<!--
* {{memoria pública|}}
* {{mcu represión|}}
-->
{{represión}}""" % (nombrepila, apellido1, apellido2, apodo, sexo, lugnacimiento, fechanacimiento and invertirfecha(fechanacimiento) or '', lugfallecimiento, fechafallecimiento and invertirfecha(fechafallecimiento) or '', lugresidencia, prof and prof.lower() or '', desc, invertirfecha(fechafallecimiento), lugfallecimiento, nombrecompleto, sexo=='Hombre' and 'represaliado' or 'represaliada', sexo=='Hombre' and 'fusilado' or 'fusilada', traducirfecha(invertirfecha(fechafallecimiento)), bio and bio or '{{expandir}}', persona)
                
                page = pywikibot.Page(pywikibot.Site("15mpedia", "15mpedia"), nombrecompleto)
                if page.exists():
                    print('Ya existe', nombrecompleto)
                    f = open('todoslosnombres-yaexiste.txt', 'a')
                    output2 = '%s\n%s' % (output, '-'*50)
                    f.write(output2)
                    f.close()
                else:
                    print(output)
                    print('-'*50)
                    page.text = output
                    page.save('BOT - Creando página', botflag=False)
                    
                    redtext = '#REDIRECT [[%s]]' % (nombrecompleto)
                    red = pywikibot.Page(pywikibot.Site("15mpedia", "15mpedia"), nombrecompleto2)
                    red.text = redtext
                    red.save('BOT - Creando redirección a [[%s]]' % (nombrecompleto), botflag=True)
            
                    time.sleep(10)
            c += 1

if __name__ == '__main__':
    main()

