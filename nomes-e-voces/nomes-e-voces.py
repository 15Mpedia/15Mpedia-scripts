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

import csv
import pywikibot
import re

def invertirfecha(fecha):
    #if len(fecha.split('/')) == 3:
    #    fecha = '%s/%s/%s' % (fecha.split('/')[2], fecha.split('/')[1], fecha.split('/')[0])
    
    fecha = fecha.replace('-', '/')
    
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

def cleanfield(s=''):
    try:
        s = unicode(s, 'utf-8')
    except:
        pass
    s = s.replace(u'Descoñecida', '')
    s = s.replace(u'Descoñecido', '')
    s = s.replace('?', '')
    s = s.strip()
    return s

def main():
    f = open('profesiones-nomesevoces-conversor.csv', 'r')
    profesiones = {}
    for x in unicode(f.read(), 'utf-8').splitlines():
        profesiones[x.split(',')[0].lower()] = x.split(',')[1].lower()
    f.close()
    
    skip = u''
    with open('nomes-e-voces.csv', 'rb') as f:
        personas = csv.reader(f, delimiter=',', quotechar='"')
        for persona in personas:
            #"Nome","Apelidos","Apodo","Suceso","Sexo","Idade","Profesión","Natural Concello","Natural Comarca","Natural Provincia","Lugar","Veciño Concello","Veciño Comarca","Veciño Provincia","Morte","Traxectoria"
            nombrepila = cleanfield(persona[0])
            apellidos = cleanfield(persona[1])
            apodo = cleanfield(persona[2])
            suceso = cleanfield(persona[3])
            sexo = cleanfield(persona[4])
            edad = cleanfield(persona[5])
            prof = cleanfield(persona[6])
            natconcello = cleanfield(persona[7])
            natcomarca = cleanfield(persona[8])
            natprovincia = cleanfield(persona[9])
            lugar = cleanfield(persona[10])
            vecconcello = cleanfield(persona[11])
            veccomarca = cleanfield(persona[12])
            vecprovincia = cleanfield(persona[13])
            fechamuerte = cleanfield(persona[14])
            trayectoria = cleanfield(persona[15])
            
            if not nombrepila or not apellidos:
                continue
            
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
            
            if sexo == 'Home':
                sexo = 'Hombre'
            elif sexo == 'Muller':
                sexo = 'Mujer'
            else:
                sexo = ''
            
            proftrad = prof
            if prof.lower() in profesiones:
                proftrad = profesiones[prof.lower()]
            proftrad = cleanfield(proftrad)
            
            if suceso not in [u"Execución", u"Paseo"]:
                continue
            if '00' in fechamuerte:
                continue
            
            bio = u''
            if natconcello:
                bio += u'%s era de [[%s]].' % (nombrepila, natconcello)
            if not proftrad:
                if edad != '0':
                     if bio:
                         bio += u' Tenía %s años cuando fue %s.' % (edad, sexo=='Hombre' and 'fusilado' or 'fusilada')
                     else:
                         bio += u'%s tenía %s años cuando fue %s.' % (nombrepila, edad, sexo=='Hombre' and 'fusilado' or 'fusilada')
            else:
                if edad != '0':
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
                bio += u'<ref name="nomesevoces" />'
            
            desc = u'%s por el franquismo, %s el %s.' % (sexo=='Hombre' and 'Represaliado' or 'Represaliada', sexo=='Hombre' and 'fusilado' or 'fusilada', traducirfecha(invertirfecha(fechamuerte)))
            
            output = u"""{{Infobox Persona
|nombre=%s
|primer apellido=%s
|segundo apellido=%s
|sexo=%s
|lugar de nacimiento=%s
|fecha de nacimiento=
|lugar de fallecimiento=
|fecha de fallecimiento=%s
|ocupación=%s
|descripción=%s
|represión={{persona represaliada
|represión=Fusilamiento
|represor=Franquismo
|fecha=%s
|lugar=
}}
}}
'''%s''', %s por el [[franquismo]], [[Lista de personas fusiladas por el franquismo|%s]] el [[%s]].<ref name="nomesevoces">{{Nomes e Voces}}</ref>

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
{{represión}}""" % (nombrepila, apellido1, apellido2, sexo, natconcello, invertirfecha(fechamuerte), proftrad and proftrad.lower() or '', desc, invertirfecha(fechamuerte), nombrecompleto, sexo=='Hombre' and 'represaliado' or 'represaliada', sexo=='Hombre' and 'fusilado' or 'fusilada', traducirfecha(invertirfecha(fechamuerte)), bio and bio or '{{expandir}}')
            
            print(output)
            
            page = pywikibot.Page(pywikibot.Site("15mpedia", "15mpedia"), nombrecompleto)
            if page.exists():
                print 'Ya existe', nombrecompleto.encode('utf-8')
                f = open('nomesevoces-yaexiste.txt', 'a')
                output2 = u'%s\n%s' % (output, '-'*50)
                f.write(output2.encode('utf-8'))
                f.close()
            else:
                print(output)
                print('-'*50)
                page.text = output
                page.save(u'BOT - Creando página', botflag=False)
                
                redtext = u'#REDIRECT [[%s]]' % (nombrecompleto)
                red = pywikibot.Page(pywikibot.Site("15mpedia", "15mpedia"), nombrecompleto2)
                red.text = redtext
                red.save(u'BOT - Creando redirección a [[%s]]' % (nombrecompleto), botflag=True)

if __name__ == '__main__':
    main()

