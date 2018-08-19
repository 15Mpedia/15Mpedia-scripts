#!/usr/bin/env python
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
import time
import urllib.parse
import urllib.request
import pywikibot
from pywikibot.specialbots import UploadRobot

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
            maxsleep = 0
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

def unquote(s):
    s = re.sub('&quot;', '"', s)
    return s

def generateInfobox(photoid, photometadata, cats, flickrseturl, flickrsetname, flickruser):
    """
    <licenses>
    <license id="0" name="All Rights Reserved" url="" />
    <license id="1" name="Attribution-NonCommercial-ShareAlike License" url="https://creativecommons.org/licenses/by-nc-sa/2.0/" />
    <license id="2" name="Attribution-NonCommercial License" url="https://creativecommons.org/licenses/by-nc/2.0/" />
    <license id="3" name="Attribution-NonCommercial-NoDerivs License" url="https://creativecommons.org/licenses/by-nc-nd/2.0/" />
    <license id="4" name="Attribution License" url="https://creativecommons.org/licenses/by/2.0/" />
    <license id="5" name="Attribution-ShareAlike License" url="https://creativecommons.org/licenses/by-sa/2.0/" />
    <license id="6" name="Attribution-NoDerivs License" url="https://creativecommons.org/licenses/by-nd/2.0/" />
    <license id="7" name="No known copyright restrictions" url="https://www.flickr.com/commons/usage/" />
    <license id="8" name="United States Government Work" url="http://www.usa.gov/copyright.shtml" />
    <license id="9" name="Public Domain Dedication (CC0)" url="https://creativecommons.org/publicdomain/zero/1.0/" />
    <license id="10" name="Public Domain Mark" url="https://creativecommons.org/publicdomain/mark/1.0/" />
    </licenses>
    """
    licenses = { "1": "cc-by-nc-sa-2.0", "2": "cc-by-nc-2.0", "3": "cc-by-nc-nd-2.0", "4": "cc-by-2.0", "5": "cc-by-sa-2.0", "6": "cc-by-nd-2.0", "9": "cc-zero-1.0"}
    desc = photometadata['title']
    if photometadata['description']:
        if desc:
            desc = '%s. %s' % (desc, photometadata['description'])
        else:
            desc = photometadata['description']
    source = '[%s %s] ([%s %s])' % (photometadata['photourl'], photometadata['title'], flickrseturl, flickrsetname)
    date = photometadata['date-taken']
    author = '{{flickr|%s}}' % (flickruser)
    license = '{{%s}}' % (licenses[photometadata['license']])
    coordinates = ''
    if photometadata['coordinates']:
        coordinates = '\n| coordenadas = %s' % (', '.join(photometadata['coordinates']))
    tags = ''
    if photometadata['tags']:
        tags = '\n| palabras clave = %s' % (', '.join(photometadata['tags']))
    output = u"""{{Infobox Archivo\n| descripción = %s\n| fuente = %s\n| fecha de creación = %s\n| autor = %s\n| licencia = %s%s%s\n}}%s""" % (desc, source, date, author, license, coordinates and coordinates or '', tags and tags or '', cats)
    return output

def getflickrapikey():
    f = open('flickrapi.key', 'r')
    flickrapikey = f.read().strip()
    return flickrapikey

def main():
    site = pywikibot.Site('15mpedia', '15mpedia')
    flickrapilimit = 500
    flickrapikey = getflickrapikey() #do not share key
    
    flickrseturl = ""
    categories = []
    tags = []
    #load parameters
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            if arg.startswith('--flickrset:'): # --flickrset:http://www.flickr.com/photos/15mmalagacc/sets/72157629844179358/
                flickrseturl = arg[12:]
            elif arg.startswith('--categories:'): # --categories:"15M_en_Madrid;Ocupa_el_Congreso"
                categories = [re.sub('_', ' ', category) for category in arg[13:].split(';')]
            elif arg.startswith('--tags:'): # --tags:"15M;Acampada_Sol"
                tags = [re.sub('_', ' ', tag) for tag in arg[7:].split(';')]
    if not flickrseturl:
        print('Provide --flickrset: parameter. Example: --flickrset:https://www.flickr.com/photos/15mmalagacc/sets/72157629844179358/')
        sys.exit()
    """if not categories:
        print('Provide --categories: parameter. Example: --categories:"15M_en_Madrid;Ocupa_el_Congreso"')
        sys.exit()"""
    
    flickrseturl = flickrseturl.replace('/sets/', '/albums/')
    flickruser = flickrseturl.split('/photos/')[1].split('/albums/')[0].strip()
    flickrsetid = flickrseturl.split('/albums/')[1].split('/')[0].strip('/').strip()
    raw = getURL(url=flickrseturl)
    m = re.findall(r'"albumId":"%s","nsid":"([^"]+?)"' % (flickrsetid), raw)
    flickeruserid = ''
    if m:
        flickeruserid = m[0]
    else:
        print("No se encontro flickeruserid")
        sys.exit()
    m = re.findall(r',"pathAlias":"([^"]+?)"', raw)
    
    #load set metadata
    apiquery = 'https://api.flickr.com/services/rest/?method=flickr.photosets.getPhotos&api_key=%s&photoset_id=%s&user_id=%s&per_page=%s&format=json&nojsoncallback=1' % (flickrapikey, flickrsetid, flickeruserid, flickrapilimit)
    jsonset = json.loads(getURL(url=apiquery))
    #print(jsonset)
    flickrsetname = jsonset["photoset"]["title"]
    flickeruser = jsonset["photoset"]["ownername"]
    photoids = [photo["id"] for photo in jsonset["photoset"]["photo"]]
    print('There are', len(photoids), 'images in the set', flickrsetid, 'by', flickruser)
    
    #load images metadata
    for photoid in photoids:
        apiquery = 'https://api.flickr.com/services/rest/?method=flickr.photos.getInfo&api_key=%s&photo_id=%s&format=json&nojsoncallback=1' % (flickrapikey, photoid)
        jsonphoto = json.loads(getURL(url=apiquery))
        
        #check license, if not free, do not donwload later
        photolicense = jsonphoto["photo"]["license"]
        if not photolicense in ["1", "2", "3", "4", "5", "6", "9"]:
            print('Skiping', photoid, 'which is not Creative Commons or Public Domain')
            continue
        
        photometadata = {
            'title': unquote("title" in jsonphoto["photo"] and jsonphoto["photo"]["title"]["_content"].strip() or ''), 
            'description': unquote("description" in jsonphoto["photo"] and jsonphoto["photo"]["description"]["_content"].strip() or ''),
            'date-taken': "taken" in jsonphoto["photo"]["dates"] and jsonphoto["photo"]["dates"]["taken"] or '', 
            'license': photolicense, 
            'coordinates': "location" in jsonphoto["photo"] and [jsonphoto["photo"]["location"]["latitude"], jsonphoto["photo"]["location"]["longitude"]] or '', 
            'localfilename': '%s - %s - %s.jpg' % (flickruser, flickrsetid, photoid), 
            'photourl': "https://www.flickr.com/photos/%s/%s/" % (flickruser, photoid), 
            'tags': [tag["raw"] for tag in jsonphoto["photo"]["tags"]["tag"]] + tags, 
        }
        photometadata['description'] = re.sub(r' *\n+ *', r'\n\n', photometadata['description'])
        if 'has uploaded' in photometadata['description']:
            photometadata['description'] = ''
        photofullres = 'https://farm%s.staticflickr.com/%s/%s_%s_o_d.jpg' % (jsonphoto["photo"]["farm"], jsonphoto["photo"]["server"], jsonphoto["photo"]["id"], jsonphoto["photo"]["originalsecret"])
        
        print(photoid)
        print(photometadata)
        print(photofullres)
        
        cats = ''
        if categories:
            cats = '\n\n%s' % ('\n'.join(['[[Categoría:%s]]' % (category) for category in categories]))
        
        output = generateInfobox(photoid, photometadata, cats, flickrseturl, flickrsetname, flickruser)
        
        #https://www.mediawiki.org/wiki/Manual:Pywikibot/upload.py
        aborts = set()
        ignorewarn = set(['duplicate']) # los duplicados los controlamos con page.exists() mas abajo
        summary = "BOT - Subiendo imagen %s" % (photometadata['photourl'])
        
        page = pywikibot.Page(site, "File:%s" % (photometadata['localfilename']))
        if page.exists():
            print("Ya existe")
            continue
        
        #print(output)
        bot = UploadRobot(photofullres, description=output, useFilename=photometadata['localfilename'], keepFilename=True, verifyDescription=False, aborts=aborts, ignoreWarning=ignorewarn, summary=summary, targetSite=site)
        bot.run()

if __name__ == '__main__':
    main()

