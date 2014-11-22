#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2013-2014 emijrp <emijrp@gmail.com>
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

import os
import re
import string
import sys
import time
import wikipedia
import zipfile

if len(sys.argv)<3:
    print 'Error, ejecuta este script asi: python votacionescongreso.py legislatura sesion'
    print 'Donde legislatura es el numero decimal de la legislatura y sesion el numero de sesion'
    print 'De momento solo hay XML de la 10 legislatura en adelante'

parlamento = u'Congreso de los Diputados'
l = sys.argv[1]
s = sys.argv[2]
url = 'http://www.congreso.es/votaciones/OpenData?sesion=%s&completa=1&legislatura=%s' % (s, l)
zipname = 'l%ss%s.zip' % (l, s)
os.system('wget -c "%s" -O %s' % (url, zipname))

legislatura = u''
if l == '10':
    legislatura = u'X Legislatura'
else:
    print 'Error legislatura'
    sys.exit()

votacionesids = []
zipfile = zipfile.ZipFile(zipname)
for zipp in zipfile.namelist():
    xmlraw = unicode(zipfile.read(zipp), 'ISO-8859-1')
    #print xmlraw
   
    sesion = re.findall(ur"(?im)<sesion>(\d+)</sesion>", xmlraw)[0]
    if sesion != s:
        print 'Error, no coinciden los numeros de sesion'
        sys.exit()
    
    numerovotacion = re.findall(ur"(?im)<numerovotacion>(\d+)</numerovotacion>", xmlraw)[0]
    votacionesids.append(int(numerovotacion))
    fecha = re.findall(ur"(?im)<fecha>([^<]+)</fecha>", xmlraw)[0]
    fecha = u'%s-%s-%s' % (fecha.split('/')[2], '%02d' % (int(fecha.split('/')[1])), '%02d' % (int(fecha.split('/')[0])))
    titulo = re.search(ur"(?im)<titulo>", xmlraw) and re.findall(ur"(?im)<titulo>([^<]+)</titulo>", xmlraw)[0] or u''
    textoexp = re.search(ur"(?im)<textoexpediente>", xmlraw) and re.findall(ur"(?im)<textoexpediente>([^<]+)</textoexpediente>", xmlraw)[0] or u''
    titulosub = re.search(ur"(?im)<titulosubgrupo>", xmlraw) and re.findall(ur"(?im)<titulosubgrupo>([^<]+)</titulosubgrupo>", xmlraw)[0] or u''
    textosub = re.search(ur"(?im)<textosubgrupo>", xmlraw) and re.findall(ur"(?im)<textosubgrupo>([^<]+)</textosubgrupo>", xmlraw)[0] or u''
    
    print sesion, numerovotacion, fecha

    asentimiento = re.search(ur"(?im)<asentimiento>", xmlraw) and re.findall(ur"(?im)<asentimiento>([^<]+)</asentimiento>", xmlraw)[0] or u''
    presentes = re.search(ur"(?im)<presentes>", xmlraw) and re.findall(ur"(?im)<presentes>([^<]+)</presentes>", xmlraw)[0] or u''
    afavor = re.search(ur"(?im)<afavor>", xmlraw) and re.findall(ur"(?im)<afavor>([^<]+)</afavor>", xmlraw)[0] or u''
    encontra = re.search(ur"(?im)<encontra>", xmlraw) and re.findall(ur"(?im)<encontra>([^<]+)</encontra>", xmlraw)[0] or u''
    abstenciones = re.search(ur"(?im)<abstenciones>", xmlraw) and re.findall(ur"(?im)<abstenciones>([^<]+)</abstenciones>", xmlraw)[0] or u''
    novotan = re.search(ur"(?im)<novotan>", xmlraw) and re.findall(ur"(?im)<novotan>([^<]+)</novotan>", xmlraw)[0] or u''
    
    print asentimiento, presentes, afavor, encontra, abstenciones, novotan
    
    votosraw = re.search(ur"(?im)<votaciones>", xmlraw) and re.findall(ur"(?im)<votacion>\s*<asiento>([^<]+)</asiento>\s*<diputado>([^<]+)</diputado>\s*(<grupo>([^<]+)</grupo>)?\s*<voto>([^<]+)</voto>\s*</votacion>", xmlraw) or []
    votos = u''
    for asiento, votante, gr, grupo, voto in votosraw:
        votos += u'{{votación voto|parlamento=%s|legislatura=%s|sesión=%s|votación=%s|asiento=%s|votante=%s|grupo=%s|voto=%s}}\n' % (parlamento, legislatura, sesion, numerovotacion, asiento, votante, grupo, voto)
    #print votos
    
    output = string.Template(u"""{{Votación información
|parlamento=$parlamento
|legislatura=$legislatura
|sesión=$sesion
|votación=$numerovotacion
|fecha=$fecha
|título=$titulo
|texto expediente=$textoexp
|título subgrupo=$titulosub
|texto subgrupo=$textosub
}}

{{Votación totales
|asentimiento=$asentimiento
|presentes=$presentes
|a favor=$afavor
|en contra=$encontra
|abstenciones=$abstenciones
|no votan=$novotan
}}
<noinclude>
{{votación votos inicio}}
$votos{{votación votos fin}}

== Enlaces externos ==
* {{votaciones congreso xml|legislatura=$l|sesión=$sesion}}

{{votaciones congreso}}</noinclude>""")
    output = output.safe_substitute({'parlamento':parlamento, 'l':l, 'legislatura':legislatura, 'sesion':sesion, 'numerovotacion':numerovotacion, 'fecha':fecha, 'titulo':titulo, 'textoexp':textoexp, 'titulosub':titulosub, 'textosub':textosub, 'asentimiento':asentimiento, 'presentes':presentes, 'afavor':afavor, 'encontra':encontra, 'abstenciones':abstenciones, 'novotan':novotan, 'votos':votos, })
    
    p = wikipedia.Page(wikipedia.Site('15mpedia', '15mpedia'), u'Lista de votaciones del Congreso de los Diputados/%s/Sesión %s/Votación %s' % (legislatura, sesion, numerovotacion))
    p.put(output, u'BOT - Creando página de votación del Congreso de los Diputados')
    time.sleep(5)
    
votaciones = u''
votacionesids.sort()
for votacionid in votacionesids:
    votaciones += u"""
=== Votación %s ===
{{main|Lista de votaciones del Congreso de los Diputados/%s/Sesión %s/Votación %s}}
{{:Lista de votaciones del Congreso de los Diputados/%s/Sesión %s/Votación %s}}
""" % (votacionid, legislatura, sesion, votacionid, legislatura, sesion, votacionid)

output = string.Template(u"""La siguiente es una '''lista de votaciones de la sesión $sesion de la $legislatura del $parlamento'''.

== Votaciones de la sesión $sesion de la $legislatura del $parlamento ==
$votaciones
== Enlaces externos ==

* {{votaciones congreso xml|legislatura=$l|sesión=$sesion}}

{{votaciones congreso}}""")
output = output.safe_substitute({'parlamento':parlamento, 'l':l, 'legislatura':legislatura, 'sesion':sesion, 'votaciones':votaciones, })
p = wikipedia.Page(wikipedia.Site('15mpedia', '15mpedia'), u'Lista de votaciones del Congreso de los Diputados/%s/Sesión %s' % (legislatura, sesion))
p.put(output, u'BOT - Creando página de votación del Congreso de los Diputados')
p.protect(editcreate='sysop', move='sysop', unprotect=False, reason=u"Protegiendo en cascada página de votaciones", editcreate_duration='infinite', move_duration='infinite', cascading=True, prompt=False, throttle=True)
