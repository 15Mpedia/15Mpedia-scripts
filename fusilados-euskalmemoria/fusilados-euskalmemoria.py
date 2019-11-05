#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2019 emijrp <emijrp@gmail.com>
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

import urllib.parse
import urllib.request
import pywikibot
import re
import sys
import time

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

def main():
    nombresmujer = []
    f = open('nombrespilamujer', 'r')
    nombresmujer = f.read().strip().splitlines()
    f.close()
    for page in range(1, 2):
        fusilados = []
        raw = ''
        url = 'http://www.euskalmemoria.eus/es/db/fusilatuak?page=%d' % (page)
        raw = getURL(url=url)
        m = re.findall(r'(?im)<tr>\s*?<td>\s*?<a [^<>]*? href="/es/db/fusilatuak/ikusi/(\d+)" [^<>]*?>([^<>]*?)</a>\s*?</td>\s*?<td>([^<>]*?)</td>\s*?<td>([^<>]*?)</td>\s*?</tr>', raw)
        for fus in m:
            url2 = 'http://www.euskalmemoria.eus/es/db/fusilatuak/ikusi/%d' % (int(fus[0]))
            raw2 = getURL(url=url2)
            fuslugar = ''
            circunstancias = ''
            n = re.findall(r'(?im)<tr>\s*?<td class="izenburua" valign="top">Lugar</td>\s*?<td class="fitxaAzalpena" valign="top">([^<>]*?)</td>\s*?</tr>\s*?<tr>\s*?<td class="izenburua" valign="top">Circunstancias</td>\s*?<td class="fitxaAzalpena" valign="top">([^<>]*?)</td>\s*?</tr>', raw2)
            if n:
                fuslugar = n[0][0]
                circunstancias = n[0][1]
            fusiladorow = [fus[0], fus[1], fus[2], fus[3], fuslugar, circunstancias]
            fusilados.append(fusiladorow)
            print(fusiladorow)
            time.sleep(10)
        g = open('fusilados-euskalmemoria.txt', 'a')
        g.write('\n'+'\n'.join([';'.join(x) for x in fusilados]))
        g.close()
    
        skip = ''
        for fusilado in fusilados:
            if skip:
                if skip == fusilado[1]:
                    skip = ''
                continue
            
            if not ', ' in fusilado[1] or not ' ' in fusilado[1]:
                continue
            
            nombrepila = fusilado[1].split(', ')[1].strip()
            apellidos = fusilado[1].split(', ')[0].strip()
            apellido1 = ''
            apellido2 = ''
            if apellidos:
                if not ' ' in apellidos:
                    apellido1 = apellidos
                elif len(apellidos.split(' ')) == 2:
                    apellido1, apellido2 = apellidos.split(' ')
                else:
                    apellido1 = apellidos.split(' ')[0]
                    apellido2 = ' '.join(apellidos.split(' ')[1:])
            nombrecompleto = '%s %s' % (nombrepila, apellidos)
            nombrecompleto2 = '%s, %s' % (apellidos, nombrepila)
            
            fechafus = fusilado[3].strip()
            resmuni = fusilado[2].strip()
            fuslugar = fusilado[4].strip()
            print(nombrecompleto, fechafus, resmuni, fuslugar)
            
            sexo = 'Hombre'
            if nombrepila in nombresmujer:
                sexo = 'Mujer'
            bio = ''
            if resmuni:
                bio += '%s era de [[%s]].' % (nombrepila, resmuni)
            
            if bio:
                bio += '<ref name="EuskalMemoria-Fusilatuak" />'
            print(bio)
            
            if fechafus:
                desc = '%s por el franquismo, %s el %s.' % (sexo=='Hombre' and 'Represaliado' or 'Represaliada', sexo=='Hombre' and 'fusilado' or 'fusilada', traducirfecha(invertirfecha(fechafus)))
            else:
                desc = '%s por el franquismo, %s.' % (sexo=='Hombre' and 'Represaliado' or 'Represaliada', sexo=='Hombre' and 'fusilado' or 'fusilada')
            print(desc)
            
            output = """{{Infobox Persona
|nombre=%s
|primer apellido=%s
|segundo apellido=%s
|sexo=%s
|lugar de nacimiento=%s
|lugar de fallecimiento=%s
|fecha de fallecimiento=%s
|lugar de residencia=%s
|descripción=%s
|represión={{persona represaliada
|represión=Fusilamiento
|represor=Franquismo
|fecha=%s
|lugar=%s
}}
}}
'''%s''', %s por el [[franquismo]], [[Lista de personas fusiladas por el franquismo|%s]]%s%s.<ref name="EuskalMemoria-Fusilatuak">{{EuskalMemoria-Fusilatuak}}</ref>

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
<!--
* {{memoria pública|}}
* {{mcu represión|}}
-->
{{represión}}""" % (nombrepila, apellido1, apellido2, sexo, resmuni, fuslugar, invertirfecha(fechafus), resmuni, desc, invertirfecha(fechafus), fuslugar, nombrecompleto, sexo=='Hombre' and 'represaliado' or 'represaliada', sexo=='Hombre' and 'fusilado' or 'fusilada', fechafus and (' el [[%s]]' % traducirfecha(invertirfecha(fechafus))) or '', fuslugar and (' en [[%s]]' % fuslugar) or '', bio and bio or '{{expandir}}')
            print(output)
            
            page = pywikibot.Page(pywikibot.Site("15mpedia", "15mpedia"), nombrecompleto)
            if page.exists() and len(page.text) > 1:
                print('Ya existe', nombrecompleto)
                f = open('fusilados-euskalmemoria-yaexiste.txt', 'a')
                output2 = '%s\n%s' % (output, '-'*50)
                f.write(output2)
                f.close()
            else:
                print(output)
                print('-'*50)
                page.text = output
                page.save(u'BOT - Creando página', botflag=True)
                
                redtext = '#REDIRECT [[%s]]' % (nombrecompleto)
                red = pywikibot.Page(pywikibot.Site("15mpedia", "15mpedia"), nombrecompleto2)
                red.text = redtext
                red.save(u'BOT - Creando redirección a [[%s]]' % (nombrecompleto), botflag=True)

if __name__ == '__main__':
    main()
