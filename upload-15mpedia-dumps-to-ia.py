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
import os
import sys

"""
Uso:

python script.py xml # Sube el dump xml de hoy

python script.py files # Sube el dump de ficheros de hoy

* Corregir las variables de path si es necesario

"""

def main():
    keyspath = './ia-keys.txt' # securize this file, get your keys from https://archive.org/account/s3.php
    dumpxmlpath = './dumps/xml' #15mpedia.org-20150408_043001.xml.7z
    dumpfilespath = './dumps/files' #15mpedia.org-files-20150408.tar
    itemname = 'wiki-15mpedia.org' # donde se subirán los ficheros
    
    if len(sys.argv) < 2:
        print u'ERROR: Falta un parámetro: xml o files'
    elif not os.path.exists(keyspath):
        print u'ERROR: No encontrado fichero de claves S3 en la ruta %s' % keyspath    
    else:
        #leer claves
        f = open(keyspath, 'r')
        keys = f.read().strip().splitlines()
        f.close()
        
        #buscar dumps
        dumptype = sys.argv[1]
        if dumptype in ['xml', 'files']:
            if dumptype == 'xml':
                listdir = os.listdir(dumpxmlpath)
                dumpxml = ''
                for filename in listdir:
                    if '15mpedia.org-%s' % (datetime.datetime.now().strftime('%Y%m%d')) in filename:
                        dumpxml = '%s/%s' % (dumpxmlpath, filename)
                
                if dumpxml:
                    print u'Subiendo dump xml... %s' % (dumpxml)
                    item = internetarchive.Item(itemname)
                    item.upload(dumpxml, access_key=keys[0], secret_key=keys[1])
                    print u'Debería aparecer en el item https://archive.org/details/%s' % (itemname)
                else:
                    print u'Dump xml no encontrado'
            
            elif dumptype == 'files':
                listdir = os.listdir(dumpfilespath)
                dumpfiles = ''
                for filename in listdir:
                    if '15mpedia.org-files-%s.tar' % (datetime.datetime.now().strftime('%Y%m%d')) in filename:
                        dumpfiles = '%s/%s' % (dumpfilespath, filename)
            
                if dumpfiles:
                    print u'Subiendo dump files... %s' % (dumpfiles)
                    item = internetarchive.Item(itemname)
                    item.upload(dumpfiles, access_key=keys[0], secret_key=keys[1])
                    print u'Debería aparecer en el item https://archive.org/details/%s' % (itemname)
                else:
                    print u'Dump files no encontrado'
            
        else:
            print u'Tipo de dump no entendido'
    
if __name__ == '__main__':
    main()
