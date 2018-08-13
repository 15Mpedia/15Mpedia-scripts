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

import pywikibot
import re

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
    f = open('fusilados-paterna.csv', 'r')
    fusilados = unicode(f.read(), 'utf-8').splitlines()[1:]
    f.close()
    f = open('nombrespilamujer', 'r')
    nombrespilamujer = unicode(f.read(), 'utf-8').splitlines()
    f.close()
    f = open('profesiones-conversor.csv', 'r')
    profesiones = {}
    for x in unicode(f.read(), 'utf-8').splitlines():
        profesiones[x.split(',')[0].lower()] = x.split(',')[1].lower()
    f.close()
    f = open('lugares-conversor.csv', 'r')
    lugares = {}
    for x in unicode(f.read(), 'utf-8').splitlines():
        lugares[x.split(',')[0]] = x.split(',')[1]
    f.close()
    
    skip = u'Jose Herrero Pastor'
    for fusilado in fusilados:
        apellidos, nombrepila, fechafus, pob, edad, prof, pobfus = fusilado.split(';')
        apellidos = apellidos.strip()
        nombrepila = nombrepila.strip()
        fechafus = fechafus.strip()
        pob = pob.strip()
        edad = edad.strip()
        prof = prof.strip()
        pobfus = pobfus.strip()        
        nombrecompleto = nombrepila + ' ' + apellidos
        if skip:
            print('Skiping', nombrecompleto)
            if nombrecompleto == skip:
                skip = ''
            continue
        nombrecompleto2 = apellidos + ', ' + nombrepila
        apellido1 = ''
        apellido2 = ''
        if len(apellidos.split(' ')) == 2:
            apellido1 = apellidos.split(' ')[0]
            apellido2 = apellidos.split(' ')[1]
        else:
            apellido1 = apellidos
            apellido2 = ''
        sexo = 'Hombre'
        if nombrepila in nombrespilamujer:
            sexo = u'Mujer'
        proftrad = prof
        if prof.lower() in profesiones:
            proftrad = profesiones[prof.lower()]
        pobtrad = pob
        if pob in lugares:
            pobtrad = lugares[pob]
        
        bio = u''
        if pob != '?':
            bio += u'%s era de %s[[%s]].' % (nombrepila, u'provincia' in pobtrad.lower() and u'la ' or u'', pobtrad)
        if proftrad == '?':
            if edad != '?':
                 if bio:
                     bio += u' Tenía %s años cuando fue %s.' % (edad, sexo=='Hombre' and 'fusilado' or 'fusilada')
                 else:
                     bio += u'%s tenía %s años cuando fue %s.' % (nombrepila, edad, sexo=='Hombre' and 'fusilado' or 'fusilada')
        else:
            if edad != '?':
                 if bio:
                     bio += u' Era %s y tenía %s años cuando fue %s.' % (proftrad.lower(), edad, sexo=='Hombre' and 'fusilado' or 'fusilada')
                 else:
                     bio += u'%s era %s y tenía %s años cuando fue %s.' % (nombrepila, proftrad.lower(), edad, sexo=='Hombre' and 'fusilado' or 'fusilada')
            else:
                 if bio:
                     bio += u' Era %s.' % (proftrad.lower())
                 else:
                     bio += u'%s era %s.' % (nombrepila, proftrad.lower())
        
        if bio:
            bio += u'<ref name="gabarda2007" />'
        
        desc = u'%s por el franquismo, %s el %s.' % (sexo=='Hombre' and 'Represaliado' or 'Represaliada', sexo=='Hombre' and 'fusilado' or 'fusilada', traducirfecha(invertirfecha(fechafus)))
        
        output = u"""{{Infobox Persona
|nombre=%s
|primer apellido=%s
|segundo apellido=%s
|sexo=%s
|lugar de fallecimiento=%s
|fecha de fallecimiento=%s
|ocupación=%s
|descripción=%s
|represión={{persona represaliada
|represión=Fusilamiento
|represor=Franquismo
|fecha=%s
|lugar=%s
}}
}}
'''%s''', %s por el [[franquismo]], [[Lista de personas fusiladas por el franquismo|%s]] el [[%s]] en [[%s]].<ref name="gabarda2007">{{Gabarda-2007}}</ref>

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
{{represión}}""" % (nombrepila, apellido1, apellido2, sexo, pobfus, invertirfecha(fechafus), proftrad != '?' and proftrad.lower() or '', desc, invertirfecha(fechafus), pobfus, nombrecompleto, sexo=='Hombre' and 'represaliado' or 'represaliada', sexo=='Hombre' and 'fusilado' or 'fusilada', traducirfecha(invertirfecha(fechafus)), pobfus, bio and bio or '{{expandir}}')
        
        page = pywikibot.Page(pywikibot.Site("15mpedia", "15mpedia"), nombrecompleto)
        if page.exists():
            print 'Ya existe', nombrecompleto.encode('utf-8')
            f = open('fusilados-paterna-yaexiste.txt', 'a')
            output2 = u'%s\n%s' % (output, '-'*50)
            f.write(output2.encode('utf-8'))
            f.close()
        else:
            print(output)
            print('-'*50)
            page.text = output
            page.save(u'BOT - Creando página', botflag=False)
            
            redtext = '#REDIRECT [[%s]]' % (nombrecompleto)
            red = pywikibot.Page(pywikibot.Site("15mpedia", "15mpedia"), nombrecompleto2)
            red.text = redtext
            red.save(u'BOT - Creando redirección a [[%s]]' % (nombrecompleto), botflag=True)
    
if __name__ == '__main__':
    main()
