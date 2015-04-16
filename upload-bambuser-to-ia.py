#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2015 emijrp
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

import datetime
import internetarchive #pip install internetarchive More info: https://pypi.python.org/pypi/internetarchive
import json
import os
import re
import sys
import time

"""
Uso:

python script.py all all # Sube todos los directorios y todos los años

python script.py all 2014 # Sube todos los directorios pero solo los ficheros de 2014

python script.py pepe all # Sube todos los años de pepe

python script.py pepe 2014 # Sube todos los ficheros de 2014 de pepe

* Corregir las variables de path si es necesario

"""

def lastmodified(f):
    t = os.path.getmtime(f)
    return datetime.datetime.fromtimestamp(t)

def errorlog(msg):
    errorlog = open('errorlog.txt', 'a')
    errorlog.write(msg.encode('utf-8'))
    errorlog.close()

def main():
    keyspath = './ia-keys.txt' # https://archive.org/account/s3.php
    dumpbambuserpath = './bambuser' # ruta al directorio de bambusers
    
    if len(sys.argv) < 3:
        print u'ERROR: Falta el parámetro usuario y el año'
        sys.exit()
    elif not os.path.exists(keyspath):
        print u'ERROR: No encontrado fichero de claves S3 en la ruta %s' % keyspath    
        sys.exit()
    else:
        #leer claves
        f = open(keyspath, 'r')
        keys = f.read().strip().splitlines()
        f.close()
        print u'Claves S3 cargadas'
        
        arguser = sys.argv[1]
        argyear = sys.argv[2]
        
        print u'Leyendo directorio %s' % dumpbambuserpath
        users = []
        for user in [x[0] for x in os.walk(dumpbambuserpath)]:
            if user.startswith('%s/' % (dumpbambuserpath)):
                users.append(unicode(user.split('/')[-1], 'utf-8'))
        print u'Se han encontrado %d directorios' % (len(users))
        users.sort()
        
        for user in users:
            if arguser != 'all' and user != arguser:
                continue
            
            print u'Recopilando archivos de %s' % (user)
            userdir = u'%s/%s' % (dumpbambuserpath, user)
            print userdir
            filestoupload = {}
            c = 0
            for file in os.listdir(userdir):
                if file.endswith('.flv'):
                    c += 1
                    fileid = file[:-4].split('-')[-1]
                    flvfile = u'%s/%s' % (userdir, file)
                    jsonfile = u'%s/%s.info.json' % (userdir, file[:-4])
                    jpgfile = u'%s/%s.jpg' % (userdir, file[:-4])
                    dumpfile = u'%s/%s.dump.json' % (userdir, file[:-4])
                    if not os.path.exists(dumpfile):
                        for file2 in os.listdir(userdir):
                            if file2.startswith(u'%s_' % fileid) and file2.endswith(u'=%s.dump' % fileid):
                                os.rename(u'%s/%s' % (userdir, file2), dumpfile)
                                break
                    
                    lmdate = lastmodified(flvfile)
                    flvyear = u'%s' % str(lmdate.year)
                    
                    if argyear == 'all':
                        if filestoupload.has_key(flvyear):
                            filestoupload[flvyear].extend([flvfile, jsonfile, jpgfile, dumpfile])
                        else:
                            filestoupload[flvyear] = [flvfile, jsonfile, jpgfile, dumpfile]
                    else:
                        if argyear == flvyear:
                            if filestoupload.has_key(flvyear):
                                filestoupload[flvyear].extend([flvfile, jsonfile, jpgfile, dumpfile])
                            else:
                                filestoupload[flvyear] = [flvfile, jsonfile, jpgfile, dumpfile]
            
            print u'Hay %d streamings en total de los anyos: %s' % (c, u', '.join(filestoupload.keys()))
            print u'Subiendo streamings del usuario %s del año %s' % (user, argyear)
            
            for year, files in filestoupload.items():
                if int(year) >= 2015:
                    print u'Ignorando ficheros del anyo %s' % (year)
                    continue
                
                itemname = u'bambuser-%s-%s' % (user, year)
                description = u'Bambuser streamings by <a href="http://bambuser.com/channel/%s">%s</a> (%s)' % (user, user, year)
                
                #capturando hashtags que empiecen con #
                tags = set()
                for filename in files:
                    f = re.sub(ur'(?i)[\.\-\,\;]', ur' ', filename.split('/')[-1])
                    for word in f.split(' '):
                        if word.startswith('#') and len(word) >= 3:
                            tags.add(word[1:])
                tags = list(tags)
                tags.sort()
                
                #descartar ficheros que no existan
                #quizas algun thumb .jpg no pudo bajarse de bambuser al ser el vídeo demasiado corto
                #ej: http://bambuser.com/v/5326177
                files2 = []
                for filename in files:
                    if os.path.exists(filename):
                        files2.append(filename.encode('utf-8'))
                    else:
                        errorlog(u'No se encontro el fichero: %s\n' % (filename))
                files = files2
                
                subject = u'spanishrevolution; bambuser; streaming; %s; %s; %s' % (user, year, ';'.join(tags)) #yes, it is ;
                originalurl = u'http://bambuser.com/channel/%s' % (user)
                item = internetarchive.get_item(itemname.encode('utf-8'))
                metadata = dict(mediatype=u'movies'.encode('utf-8'), creator=user.encode('utf-8'), collection='spanishrevolution'.encode('utf-8'), description=description.encode('utf-8'), date=year.encode('utf-8'), subject=subject.encode('utf-8'), language=u'Spanish'.encode('utf-8'), originalurl=originalurl.encode('utf-8'), year=year.encode('utf-8'), )
                item.upload(files, metadata=metadata, access_key=keys[0], secret_key=keys[1])
                print u'Deberían aparecer en https://archive.org/details/bambuser-%s-%s' % (user, year)
            
if __name__ == '__main__':
    main()
