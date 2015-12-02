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

import csv
import pywikibot
import re
import urllib

def getwhitelist():
    #load user whitelist
    raw = urllib.request.urlopen('https://raw.githubusercontent.com/15Mpedia/15Mpedia-scripts/master/games/imagetag/whitelist.txt').readall()
    whitelist = [x.decode("utf-8") for x in raw.splitlines()]
    print(len(whitelist),'users in whitelist')
    return whitelist

def main():
    csvtweets = '../imagetag-tweets.csv'
    csvreplies = '../imagetag-replies.csv'
    whitelist = getwhitelist()
    
    #cargar todos los tweets
    tweets = []
    f = csv.reader(open(csvtweets, 'r'), delimiter='|', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for row in f:
        tweets.append(row)
    
    #cargar todos los replies
    replies = []
    f = csv.reader(open(csvreplies, 'r'), delimiter='|', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for row in f:
        replies.append(row)
    
    #extraer palabras de los tweets
    wiki = {}
    for tweetid, filename, text in tweets:
        if not filename in wiki:
            wiki[filename] = []
        for replyid, replyauthor, replyto, replytext in replies:
            if not replyauthor in whitelist:
                continue
            if not replyto in [tweet[0] for tweet in tweets]:
                continue
            if not replytext.startswith('@'):
                continue
            
            if replyto == tweetid:
                temp = ' '.join(replytext.split(' ')[1:]).split(',')
                keywords = []
                for k in temp:
                    keyword = k.strip()
                    if len(keyword) < 3:
                        continue
                    keywords.append(keyword)
                keywords.sort()
                wiki[filename] += keywords
    
    #comparar con las palabras del wiki
    for filename, keywordstweets in wiki.items():
        print('\n','#'*30,'\nAnalysing:',filename,'\n','#'*30,'\n')
        filepage = pywikibot.Page(pywikibot.Site("15mpedia", "15mpedia"), 'File:%s' % (filename))
        m = re.findall(r'(?im)\|\s*palabras clave\s*=\s*([^\n\|]*?)\s*\n', filepage.text)
        keywordswiki = set([])
        if m:
            for n in m[0].split(','):
                keywordswiki.add(n.strip())
        print('Keywords in wiki:',keywordswiki)
        keywordstweets = set(keywordstweets)
        print('Keywords in tweets:',keywordstweets)
        adding = list(keywordstweets-keywordswiki)
        adding.sort()
        if adding:
            print('Adding:',adding)
            keywords = list(keywordstweets.union(keywordswiki))
            keywords.sort()
            newtext = ''
            if re.search(r'(?im)\|\s*palabras clave\s*=', filepage.text):
                newtext = re.sub(r'(?im)\|\s*palabras clave\s*=\s*[^\|\n]*?\n', r'|palabras clave=%s\n' % ', '.join(keywords), filepage.text)
            else:
                newtext = re.sub(r'(?im)(\|\s*[^\|=]+\s*=[^\n]*?\n)(\}\})', r'\1|palabras clave=%s\n\2' % ', '.join(keywords), filepage.text)
            pywikibot.showDiff(filepage.text, newtext)
            filepage.text = newtext
            filepage.save('BOT - Añadiendo palabras clave: %s' % (', '.join(adding)), botflag=False)
        else:
            print('Nothing to add')

if __name__ == '__main__':
    main()
