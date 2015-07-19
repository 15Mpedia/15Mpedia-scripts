#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2015 emijrp <emijrp@gmail.com>
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

import json
import os
import re
import sys
import pywikibot

def main():
    if len(sys.argv) != 2:
        print 'script.py [year]'
        sys.exit()
    year = sys.argv[1]
    print 'Leyendo partidos de', year
    f = open('parties.json', 'r')
    partidos = json.loads(f.read())
    f.close()
    
    for pid, props in partidos.items():
        if pid == 'organization':
            continue
        
        #print pid
        #print props
        
        tipo = props.has_key('tipoFormacion') and props['tipoFormacion'] or ''
        siglas = props.has_key('siglas') and props['siglas'] or ''
        nombre = props.has_key('nombre') and props['nombre'] or ''
        fecha = props.has_key('fecInscripcion') and props['fecInscripcion'] or ''
        ambito = props.has_key('ambito') and props['ambito'] or ''
        simbolo = props.has_key('simbolo') and props['simbolo'] or ''
        
        nombre2 = []
        for s in nombre.split(' '):
            if len(s) <= 3:
                nombre2.append(u'%s' % (s.lower()))
            else:
                nombre2.append(u'%s%s' % (s[0].upper(), s[1:].lower()))
        nombre = u' '.join(nombre2)
        
        if tipo.lower() == 'partido politico':
            tipo = u'Partido político'
        
        if ambito.lower() == 'autonomico':
            ambito = u'Autonómico'
        
        if fecha:
            fecha = fecha.split('/')
            fecha = '%s/%s/%s' % (fecha[2], fecha[1], fecha[0])
        
        if not fecha.startswith(year):
            continue
        
        infobox = u"""{{Infobox Partido político
|nombre=%s
|siglas=%s
|país=España
|tipo de formación=%s
|fecha de inscripción=%s
|ámbito territorial=%s
}}""" % (nombre, siglas, tipo, fecha, ambito)
        
        print '\n', '#'*40, '\n', nombre, '\n', '#'*40, '\n'
        print infobox
        
        page = pywikibot.Page(pywikibot.Site('15mpedia', '15mpedia'), u'%s' % (nombre))
        if page.exists():
            print 'La pagina ya existe'
            continue
        else:
            page.text = infobox
            page.save(u'BOT - Creando partido político', botflag=False)

if __name__ == '__main__':
    main()

