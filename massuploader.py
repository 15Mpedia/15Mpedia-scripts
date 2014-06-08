#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2012-2014 emijrp <emijrp@gmail.com>
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

# Install: save this script in the pywikipedia directory
# Usage: python massuploader.py --botname:MiBot --flickrset:https://www.flickr.com/photos/15mmalagacc/sets/72157629844179358/ --importimagesphp:/path/to/importImages.php --categories:"15M_en_Madrid;Ocupa_el_Congreso" --mode:import/url
# More documentation: http://www.mediawiki.org/wiki/Manual:ImportImages.php

import os
import re
import sys
import time
import urllib, urllib2
import wikipedia

def unquote(s):
    s = re.sub('&quot;', '"', s)
    return s

def generateInfobox(photoid, photometadata, cats, flickrseturl, flickrsetname, flickruser):
    desc = photometadata['title']
    if photometadata['description']:
        if desc:
            desc = u'%s. %s' % (desc, photometadata['description'])
        else:
            desc = photometadata['description']
    source = u'[%s %s] ([%s %s])' % (photometadata['photourl'], photometadata['title'], flickrseturl, flickrsetname)
    date = photometadata['date-taken']
    author = u'{{flickr|%s}}' % (flickruser)
    license = u'{{cc-%s}}' % (photometadata['license'])
    coordinates = u''
    if photometadata['coordinates'][0] and photometadata['coordinates'][1]:
        coordinates = u'\n| coordenadas = %s' % (', '.join(photometadata['coordinates']))
    output = u"""{{Infobox Archivo\n| descripción = %s\n| fuente = %s\n| fecha de creación = %s\n| autor = %s\n| licencia = %s%s\n}}%s""" % (desc, source, date, author, license, coordinates and coordinates or '', cats)
    return output

def main():
    photosmetadata = {}
    categories = []
    botname = ''
    flickrseturl = ''
    importimagesphp = ''
    mode = ''
    extra = ''
    
    #load parameters
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            if arg.startswith('--botname:'): # --botname:MiBot
                botname = arg[10:]
            elif arg.startswith('--flickrset:'): # --flickrset:http://www.flickr.com/photos/15mmalagacc/sets/72157629844179358/
                flickrseturl = arg[12:]
            elif arg.startswith('--importimagesphp:'): # --importimagesphp:/path/to/importImages.php
                importimagesphp = arg[18:]
            elif arg.startswith('--categories:'): # --categories:"15M_en_Madrid;Ocupa_el_Congreso"
                categories = [re.sub('_', ' ', unicode(category, 'utf-8')) for category in arg[13:].split(';')]
            elif arg.startswith('--mode:'): # --mode:import/url (import = server side using import.php; url = using upload.py of pywikipediabot)
                mode = arg[7:]
            elif arg.startswith('--extra:'): # --extra:extraoption
                extra = arg[8:]
    
    if not botname:
        print 'Provide --botname: parameter. Example: --botname:MiBot'
        sys.exit()
    if not flickrseturl:
        print 'Provide --flickrset: parameter. Example: --flickrset:https://www.flickr.com/photos/15mmalagacc/sets/72157629844179358/'
        sys.exit()
    if not mode:
        print 'Provide --mode: parameter. Example: import/url (import = server side using import.php; url = using upload.py of pywikipediabot)'
        sys.exit()
    if mode == 'import' and not importimagesphp:
        print 'Provide --importimagesphp: parameter. Example: --importimagesphp:/path/to/importImages.php'
        sys.exit()
    if mode == 'url' and not os.path.exists('upload.py'):
        print 'upload.py script of pywikipediabot not found'
        sys.exit()
    if not categories:
        print 'Provide --categories: parameter. Example: --categories:"15M_en_Madrid;Ocupa_el_Congreso"'
        sys.exit()
    
    flickrsetid = flickrseturl.split('/sets/')[1].split('/')[0]
    
    #load flickr set metadata
    html = unicode(urllib.urlopen(flickrseturl).read(), 'utf-8')
    pages = re.search(ur'(?im)<div class="Results">\((\d+) ', html) and int(re.findall(ur'(?im)<div class="Results">\((\d+) ', html)[0])/72 + 1 or 1 # +1 para los picos
    flickrsetname = unquote(re.findall(ur'(?im)<meta property="og:title" content="([^>]*?)" />', html)[0])
    flickruser = re.findall(ur'(?im)<meta property="flickr_photos:by" content="https?://www.flickr.com/photos/([^/]+?)/" />', html)[0]
    photoids = re.findall(ur'(?im)data-photo-id="(\d+)"', html)
    for page in range(2, pages+1): # + 1 para que el range llegue hasta el valor de pages
        html = unicode(urllib.urlopen('%s?page=%d' % (flickrseturl, page)).read(), 'utf-8')
        photoids += re.findall(ur'(?im)data-photo-id="(\d+)"', html)
    print 'There are', len(photoids), 'images in the set', flickrsetid, 'by', flickruser
    
    #load flickr images metadata
    for photoid in photoids:
        photourl = 'https://www.flickr.com/photos/%s/%s/' % (flickruser, photoid)
        html2 = unicode(urllib.urlopen(photourl).read(), 'utf-8')
        #check license, if not free, do not donwload later
        photolicense = ''
        if re.search(ur'(?im)<a href="https?://creativecommons.org/licenses/(by(-sa)?/2.0)[^=]*?" rel="license cc:license">', html2):
            photolicense = re.sub('/', '-', re.findall(ur'(?im)<a href="https?://creativecommons.org/licenses/(by(-sa)?/2.0)[^=]*?" rel="license cc:license">', html2)[0][0])
        else:
            print 'Skiping', photoid, 'which is not Creative Commons'
            continue
        
        photosmetadata[photoid] = {
            'title': re.search(ur'<meta property="og:title" content="([^>]*?)" />', html2) and unquote(re.findall(ur'<meta property="og:title" content="([^>]*?)" />', html2)[0]).strip() or '',
            'description': re.search(ur'<meta property="og:description" content="([^>]*?)" />', html2) and unquote(re.findall(ur'<meta property="og:description" content="([^>]*?)" />', html2)[0]).strip() or '', 
            'date-taken': re.search(ur'(?im)/date-taken/(\d+/\d+/\d+)', html2) and re.sub('/', '-', re.findall(ur'(?im)/date-taken/(\d+/\d+/\d+)', html2)[0]) or '', 
            'license': photolicense, 
            'coordinates': [re.search(ur'<meta property="flickr_photos:location:latitude" content="([^>]*?)" />', html2) and unquote(re.findall(ur'<meta property="flickr_photos:location:latitude" content="([^>]*?)" />', html2)[0]).strip() or '', re.search(ur'<meta property="flickr_photos:location:longitude" content="([^>]*?)" />', html2) and unquote(re.findall(ur'<meta property="flickr_photos:location:longitude" content="([^>]*?)" />', html2)[0]).strip() or ''],
            'localfilename': u'%s - %s - %s.jpg' % (flickruser, flickrsetid, photoid),
            'photourl': photourl,
        }
        if 'has uploaded' in photosmetadata[photoid]['description']:
            photosmetadata[photoid]['description'] = ''
            
        print photoid
        print photosmetadata[photoid]
        #break
    
    #choose a mode to upload
    if mode == 'url':
        for photoid, photometadata in photosmetadata.items(): #this dictionary includes only CC pics
            photourl = 'https://www.flickr.com/photos/%s/%s/sizes/o/in/set-%s/' % (flickruser, photoid, flickrsetid)
            html3 = unicode(urllib.urlopen(photourl).read(), 'utf-8')
            photourl2 = re.findall(ur'(?im)<dt>[^<]+?</dt>\s*<dd>\s*<a href="(https?://[^\">]+?)">', html3)[0]
            
            cats = u''
            if categories:
                cats = u'\n\n%s' % ('\n'.join([u'[[Categoría:%s]]' % (category) for category in categories]))
            output = generateInfobox(photoid, photometadata, cats, flickrseturl, flickrsetname, flickruser)
            #wikipedia.output(output)
            #https://www.mediawiki.org/wiki/Manual:Pywikibot/upload.py
            os.system('python upload.py -lang:15mpedia -family:15mpedia -keep -filename:"%s" -noverify "%s" "%s"' % (photometadata['localfilename'].encode('utf-8'), photourl2.encode('utf-8'), output.encode('utf-8')))
    
    elif mode == 'import':
        #download flickr images
        savepath = flickrsetid
        if not os.path.exists(savepath): #create subdirectory to save images there
            os.makedirs(savepath)
        
        for photoid, photometadata in photosmetadata.items(): #this dictionary includes only CC pics
            photourl = 'https://www.flickr.com/photos/%s/%s/sizes/o/in/set-%s/' % (flickruser, photoid, flickrsetid)
            html3 = unicode(urllib.urlopen(photourl).read(), 'utf-8')
            photourl2 = re.findall(ur'(?im)<dt>[^<]+?</dt>\s*<dd>\s*<a href="(https?://[^\">]+?)">', html3)[0]
            print 'Downloading', photometadata['localfilename'], 'from', photourl2
            try:
                urllib.urlretrieve(photourl2, savepath+'/'+photometadata['localfilename'])
            except:
                time.sleep(10)
                try:
                    urllib.urlretrieve(photourl2, savepath+'/'+photometadata['localfilename'])
                except:
                    print 'Error while retrieving image, retry'
                    sys.exit()
            #break
        
        #import images
        os.system('php %s ./%s --user=%s --comment="" %s' % (importimagesphp, flickrsetid, botname, extra))
        
        #create image pages
        cats = u''
        if categories:
            cats = u'\n\n%s' % ('\n'.join([u'[[Categoría:%s]]' % (category) for category in categories]))
        for photoid, photometadata in photosmetadata.items():
            output = generateInfobox(photoid, photometadata, cats, flickrseturl, flickrsetname, flickruser)
            wikipedia.output(output)
            p = wikipedia.Page(wikipedia.Site('15mpedia', '15mpedia'), u'File:%s' % (photometadata['localfilename']))
            p.put(output, u'BOT - Importing file')

if __name__ == '__main__':
    main()

