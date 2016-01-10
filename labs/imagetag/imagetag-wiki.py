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

import csv
import pywikibot
import re
import urllib

def getwhitelist():
    #load user whitelist
    raw = urllib.request.urlopen('https://raw.githubusercontent.com/15Mpedia/15Mpedia-scripts/master/labs/imagetag/whitelist.txt').readall()
    whitelist = [x.decode("utf-8") for x in raw.splitlines()]
    print(len(whitelist),'users in whitelist')
    return whitelist

def getbadwords():
    #load words in badwords list
    raw = urllib.request.urlopen('https://raw.githubusercontent.com/15Mpedia/15Mpedia-scripts/master/labs/imagetag/badwords.txt').readall()
    badwords = [x.decode("utf-8").lower() for x in raw.splitlines()]
    print(len(badwords),' badwords')
    return badwords

def extractkeywords(replytext, badwords):
    keywords = []
    temp = re.sub(',', ' ', replytext)
    temp = ' '.join(temp.split(' ')[1:]).split(' ') # remove "@15MpediaLabs " prefix
    for k in temp:
        k = re.sub('_', ' ', k.strip())
        if not k.startswith('#') or len(k) <= 2: #   #BN (blanco y negro) es tag tipico
            continue
        k = k[1:] # remove first #
        if not k in keywords and k.lower() not in badwords:
            keywords.append(k)
    keywords.sort()
    return keywords

def main():
    csvtweets = '../imagetag-tweets.csv'
    csvreplies = '../imagetag-replies.csv'
    whitelist = getwhitelist()
    badwords = getbadwords()
    
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
    
    #extraer keywords de los tweets
    files = {}
    tweetids = [tweet[0] for tweet in tweets]
    for tweetid, filename, tweettext in tweets:
        if filename == 'filename':
            continue
        if not filename in files:
            files[filename] = {'tweetid': set([]), 'keywordstweets': set([])}
        for replyid, replyauthor, replyto, replytext in replies:
            if not replyauthor in whitelist:
                continue
            if not replyto in tweetids:
                continue
            if not replytext.startswith('@') and not replytext.startswith('.@'):
                continue
            
            if replyto == tweetid:
                keywords = extractkeywords(replytext, badwords)
                files[filename]['tweetid'].add(replyto)
                files[filename]['keywordstweets'] = files[filename]['keywordstweets'].union(set(keywords))
    
    #comparar con las keywords del wiki
    for filename, v in files.items():
        keywordstweets = v['keywordstweets']
        tweetid = v['tweetid']
        print('\n','#'*30,'\nAnalysing:',filename,'\n','#'*30,'\n')
        filepage = pywikibot.Page(pywikibot.Site("15mpedia", "15mpedia"), 'File:%s' % (filename))
        m = re.findall(r'(?im)\|\s*palabras clave\s*=\s*([^\n\|]*?)\s*\n', filepage.text)
        keywordswiki = set([])
        if m:
            for n in m[0].split(','):
                keywordswiki.add(n.strip())
        print('Keywords in wiki:',keywordswiki)
        print('Keywords in tweets:',keywordstweets)
        adding = list(keywordstweets-keywordswiki)
        adding.sort()
        #si hay alguna nueva, se añade
        if adding:
            print('Adding:',adding)
            keywords = list(keywordstweets.union(keywordswiki))
            keywords.sort()
            newtext = filepage.text
            
            #add keywords
            if re.search(r'(?im)\|\s*palabras clave\s*=', newtext):
                newtext = re.sub(r'(?im)\|\s*palabras clave\s*=\s*[^\|\n]*?\n', r'|palabras clave=%s\n' % ', '.join(keywords), newtext)
            else:
                newtext = re.sub(r'(?im)(\|\s*[^\|=]+\s*=[^\n]*?\n)(\}\})', r'\1|palabras clave=%s\n\2' % ', '.join(keywords), newtext)
            
            #add Labs tweet id
            if re.search(r'(?im)\|\s*labs palabras clave twitter\s*=', newtext):
                m = re.findall(r'(?im)\|\s*labs palabras clave twitter\s*=\s*([^\|\n]*?)\n', newtext)
                if m:
                    temp = set([x.strip() for x in m[0].strip().split(',')])
                    temp = list(temp.union(tweetid))
                    temp.sort()
                    newtext = re.sub(r'(?im)\|\s*labs palabras clave twitter\s*=\s*[^\|\n]*?\n', '|labs palabras clave twitter=%s\n' % (', '.join(temp)), newtext)
            else:
                temp = list(tweetid)
                temp.sort()
                newtext = re.sub(r'(?im)(\|\s*[^\|=]+\s*=[^\n]*?\n)(\}\})', r'\1|labs palabras clave twitter=%s\n\2' % (', '.join(temp)), newtext)
            
            pywikibot.showDiff(filepage.text, newtext)
            filepage.text = newtext
            filepage.save('BOT - Añadiendo palabras clave: %s' % (', '.join(adding)), botflag=True)
        else:
            print('Nothing to add')

if __name__ == '__main__':
    main()
