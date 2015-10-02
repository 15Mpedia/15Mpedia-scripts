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

import csv
import os
import re
import sys
import pywikibot
import upload

""" Bot para subir las imagenes donadas por el proyecto Foto Spanish Revolution """

def main():
    site = pywikibot.Site('15mpedia', '15mpedia')
    
    mypath = 'foto-spanish-revolution'
    onlyfiles = [ f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath,f)) ]
    onlyfiles2 = {}
    for f in onlyfiles:
        f = unicode(f, 'utf-8')
        onlyfiles2[f.split('.jpg')[0].split('_')[-1]] = f
    onlyfiles = onlyfiles2
    
    #id,IdGuid,IdUser,IdSection,Author,Title,DateShot,Description,Active,DateUp,DateActive, OriginalWidth,OriginalHeight,NormalWidth,NormalHeight,SlideWidth,SlideHeight,MiniatureWidth, MiniatureHeight,OriginalName,Extension,Cesion,Creative,c15Mcc,FileName,YearShot,MonthShot,DayShot,NameAuthor,Username,WebSite,link
    
    #227,{3B8B10D1-0ABE-4748-8D74-5BB9EE8ED0AB},53,1,Juan M.P.,Sin Título,2011-05-15 00:00:00.0000000,,True,2012-04-03 03:33:20.4618795,,1909,2863,683,1024,400,600,48,72,E:\kunden\homepages\31\d407833084\www\wwwdotpichicoladotes\TempPath\0.jpg,.jpg,True,True,True,3B8B10D1-0ABE-4748-8D74-5BB9EE8ED0AB.jpg,2011,5,15,Juan M.,juanplaza,http://www.flickr.com/photos/juanplaza/,http://fotospanishrevolution.org/Fullscreen/Fullscreen.aspx?view=2&id=FAB9096B-3CB5-410B-A98B-E1EB867B287F&first=3B8B10D1-0ABE-4748-8D74-5BB9EE8ED0AB&order=
    
    with open('foto-spanish-revolution.csv', 'rb') as csvfile:
        content = csv.reader(csvfile, delimiter=',', quotechar='"')
        c = 0
        for row in content:
            c += 1
            if c==1:
                continue
            
            author = unicode(row[4], 'utf-8')
            title = unicode(row[5], 'utf-8')
            title = title.strip('.')
            title = re.sub('[\[\]]', '', title)
            dateshot = row[6].split('.')[0]
            if dateshot.endswith(' 00:00:00'):
                dateshot = dateshot.split(' 00:00:00')[0]
            description = unicode(row[7], 'utf-8')
            
            if title:
                if description:
                    desc = u'%s. %s' % (title, description)
                else:
                    desc = title
            else:
                if description:
                    desc = description
                else:
                    desc = u''
            
            dateupload = row[9].split('.')[0]
            if dateupload.endswith(' 00:00:00'):
                dateupload = dateupload.split(' 00:00:00')[0]
            
            creative = row[22] == 'True' and True or False
            filename = row[24]
            authorname = unicode(row[28], 'utf-8')
            authornick = unicode(row[29], 'utf-8')
            authorweb = row[30]
            if authorweb and not authorweb.startswith('http'):
                authorweb = 'http://%s' % (authorweb)
            photourl = row[31]
            authorid = photourl.split('&id=')[1].split('&')[0]
            photoid = photourl.split('&first=')[1].split('&')[0]
            
            authorline = u'[http://fotospanishrevolution.org/viewsection.aspx?view=2&id=%s %s]' % (authorid, author)
            if authorweb:
                authorline += u' ([%s sitio web])' % (authorweb)
            
            if creative:
                print '-'*50
                print 'La imagen es CC'
                print photoid
                print photourl
                licencia = u'{{cc-by-nc-nd-2.5}}'
                
                infobox = u"""{{Infobox Archivo
|descripción=%s
|fuente=[%s %s] en [[Foto Spanish Revolution]]
|fecha de creación=%s
|fecha de publicación=%s
|autor=%s
|licencia=%s
|donación=FotoSpanishRevolution2015
}}""" % (desc, photourl, title, dateshot, dateupload, authorline, licencia)
                #print infobox
                
                if onlyfiles.has_key(photoid):
                    imagename = u'FotoSpanishRevolution - %s - %s.jpg' % (authornick, photoid)
                    print 'Importing here https://15mpedia.org/wiki/Archivo:%s' % (re.sub(' ', '_', imagename))
                
                    imagepage = pywikibot.Page(site, u'File:%s' % imagename)
                    if imagepage.exists():
                        print 'La pagina de imagen File:%s ya existe. No subimos' % (imagename)
                        continue
                    
                    filepath = u'foto-spanish-revolution/%s' % onlyfiles[photoid]
                    bot = upload.UploadRobot([filepath], description=infobox, useFilename=imagename, keepFilename=True, verifyDescription=False, targetSite=site, uploadByUrl=False, ignoreWarning=['duplicate'])
                    bot.run()
            else:
                print '-'*50
                print 'La imagen NO es CC, saltando'
                print photourl

if __name__ == '__main__':
    main()
