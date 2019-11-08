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
            sleep = 5 # seconds
            maxsleep = 5
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

def traducirfecha2(fecha):
    trad = fecha
    meses = {'enero':1,'febrero':2,'marzo':3,'abril':4,'mayo':5,'junio':6,'julio':7,'agosto':8,'septiembre':9,'octubre':10,'noviembre':11,'diciembre':12}
    if len(fecha.split(' de ')) == 3:
        try:
            trad = '%d-%02d-%02d' % (int(fecha.split(' de ')[2]), meses[fecha.split(' de ')[1].lower()], int(fecha.split(' de ')[0]))
        except:
            trad = fecha
    
    return trad

def main():
    urls = [
    'https://web.archive.org/web/20130611040744/http://todoslosnombres.es/modules.php?name=Encyclopedia&op=terms&eid=1&ltr=A', 
    'https://web.archive.org/web/20130611040744/http://todoslosnombres.es/modules.php?name=Encyclopedia&op=terms&eid=1&ltr=B', 
    'https://web.archive.org/web/20130611040744/http://todoslosnombres.es/modules.php?name=Encyclopedia&op=terms&eid=1&ltr=C', 
    'https://web.archive.org/web/20130611040744/http://todoslosnombres.es/modules.php?name=Encyclopedia&op=terms&eid=1&ltr=D', 
    'https://web.archive.org/web/20130611040744/http://todoslosnombres.es/modules.php?name=Encyclopedia&op=terms&eid=1&ltr=E', 
    'https://web.archive.org/web/20130611040744/http://todoslosnombres.es/modules.php?name=Encyclopedia&op=terms&eid=1&ltr=F', 
    'https://web.archive.org/web/20130611040744/http://todoslosnombres.es/modules.php?name=Encyclopedia&op=terms&eid=1&ltr=G', 
    'https://web.archive.org/web/20130611040744/http://todoslosnombres.es/modules.php?name=Encyclopedia&op=terms&eid=1&ltr=H', 
    'https://web.archive.org/web/20130611040744/http://todoslosnombres.es/modules.php?name=Encyclopedia&op=terms&eid=1&ltr=I', 
    'https://web.archive.org/web/20130611040744/http://todoslosnombres.es/modules.php?name=Encyclopedia&op=terms&eid=1&ltr=J', 
    'https://web.archive.org/web/20130611040744/http://todoslosnombres.es/modules.php?name=Encyclopedia&op=terms&eid=1&ltr=K', 
    'https://web.archive.org/web/20130611040744/http://todoslosnombres.es/modules.php?name=Encyclopedia&op=terms&eid=1&ltr=L', 
    'https://web.archive.org/web/20130611040744/http://todoslosnombres.es/modules.php?name=Encyclopedia&op=terms&eid=1&ltr=M', 
    'https://web.archive.org/web/20130611040744/http://todoslosnombres.es/modules.php?name=Encyclopedia&op=terms&eid=1&ltr=N', 
    'https://web.archive.org/web/20130611040744/http://todoslosnombres.es/modules.php?name=Encyclopedia&op=terms&eid=1&ltr=O', 
    'https://web.archive.org/web/20130611040744/http://todoslosnombres.es/modules.php?name=Encyclopedia&op=terms&eid=1&ltr=P', 
    'https://web.archive.org/web/20130611040744/http://todoslosnombres.es/modules.php?name=Encyclopedia&op=terms&eid=1&ltr=Q', 
    'https://web.archive.org/web/20130611040744/http://todoslosnombres.es/modules.php?name=Encyclopedia&op=terms&eid=1&ltr=R', 
    'https://web.archive.org/web/20130611040744/http://todoslosnombres.es/modules.php?name=Encyclopedia&op=terms&eid=1&ltr=S', 
    'https://web.archive.org/web/20130611040744/http://todoslosnombres.es/modules.php?name=Encyclopedia&op=terms&eid=1&ltr=T', 
    'https://web.archive.org/web/20130611040744/http://todoslosnombres.es/modules.php?name=Encyclopedia&op=terms&eid=1&ltr=U', 
    'https://web.archive.org/web/20130611040744/http://todoslosnombres.es/modules.php?name=Encyclopedia&op=terms&eid=1&ltr=V', 
    'https://web.archive.org/web/20130611040744/http://todoslosnombres.es/modules.php?name=Encyclopedia&op=terms&eid=1&ltr=W', 
    'https://web.archive.org/web/20130611040744/http://todoslosnombres.es/modules.php?name=Encyclopedia&op=terms&eid=1&ltr=Y', 
    'https://web.archive.org/web/20130611040744/http://todoslosnombres.es/modules.php?name=Encyclopedia&op=terms&eid=1&ltr=Z', 
    ]
    skip = '1387003'
    for url in urls:
        raw = ''
        print(url)
        raw = getURL(url=url)
        m = re.findall(r'(?im)tid=(\d+)">([^<>]*?)</a></td></tr>', raw)
        for personaid, personanombre in m:
            personaid = str(personaid).strip()
            if skip:
                print('Skiping', personaid)
                if skip == personaid:
                    skip = ''
                continue
            url2 = 'https://web.archive.org/web/20130611041005/http://todoslosnombres.es/modules.php?name=Encyclopedia&op=content&tid=%s' % (personaid)
            raw2 = getURL(url=url2)
            if not raw2:
                time.sleep(5)
                raw2 = getURL(url=url2)
                if not raw2:
                    h = open('tln-asturias-errors.txt', 'a')
                    h.write('\n%s' % (url2))
                    h.close()
                    continue
            nombre = re.findall(r'(?im)<font class="title">([^<>]*?)</font>', raw2)[0].strip()
            causamuerte = re.findall(r'(?im)<strong>\s*?Causa de la muerte:\s*?</strong>([^<>]*?)<', raw2)[0].strip()
            lugarmuerte = re.findall(r'(?im)<strong>\s*?Lugar:\s*?</strong>([^<>]*?)<', raw2)[0].strip()
            fechamuerte = re.findall(r'(?im)<strong>\s*?Fecha fallecimiento:\s*?</strong>([^<>]*?)<', raw2)[0].strip()
            fechamuerteiso = traducirfecha2(fechamuerte)
            lugarnacimiento = re.findall(r'(?im)<strong>\s*?Nacimiento:\s*?</strong>([^<>]*?)<', raw2)[0].strip()
            lugarresidencia = re.findall(r'(?im)<strong>\s*?Residencia:\s*?</strong>([^<>]*?)<', raw2)[0].strip()
            edad = re.findall(r'(?im)<strong>\s*?Edad:\s*?</strong>([^<>]*?)<', raw2)[0].strip()
            edad = edad.split('años')[0].strip()
            estadocivil = re.findall(r'(?im)<strong>\s*?Estado civil:\s*?</strong>([^<>]*?)<', raw2)[0].strip()
            padres = re.findall(r'(?im)<strong>\s*?Padres:\s*?</strong>([^<>]*?)<', raw2)[0].strip()
            profesion = re.findall(r'(?im)<strong>\s*?Profesión:\s*?</strong>([^<>]*?)<', raw2)[0].strip()
            personarow = [personaid, nombre, causamuerte, lugarmuerte, fechamuerteiso, lugarnacimiento, lugarresidencia, edad, estadocivil, padres, profesion]
            print(personarow)
            g = open('tln-asturias.txt', 'a')
            g.write('\n'+';'.join(personarow))
            g.close()
            time.sleep(1)

if __name__ == '__main__':
    main()
