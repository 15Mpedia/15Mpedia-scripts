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

import catlib
import pagegenerators
import re
import urllib
import wikipedia

def main():
    site = wikipedia.Site('15mpedia', '15mpedia')
    cat = catlib.Category(site, u"Category:Streamings embebidos")
    gen = pagegenerators.CategorizedPageGenerator(cat)
    pre = pagegenerators.PreloadingGenerator(gen, pageNumber=200)
    
    users = {}
    for page in pre:
        wtitle = page.title()
        if not wtitle.startswith('Archivo:Bambuser - '):
            continue
        print '===', wtitle, '==='
        wtext = page.get()
        
        usuarioactual = re.findall(ur"(?im)\|embebido usuario=([^\r\n]+)\r\n", wtext)[0]
        print usuarioactual
        
        if not users.has_key(usuarioactual.lower()):
            channel = 'http://bambuser.com/channel/%s' % (re.sub(u" ", u"+", usuarioactual.lower()))
            raw = urllib.urlopen(channel).read()
            webusername = re.findall(ur"(?im)<span class=\"username\" title=\"([^<>]+?)\"></span>", raw)[0]
            users[usuarioactual.lower()] = webusername
        
        if users[usuarioactual.lower()] == usuarioactual:
            print 'Correcto'
        else:
            print 'Hay que trasladar'
            newtext = wtext
            newtext = re.sub(ur"(?im)\|embebido usuario=%s" % (usuarioactual.lower()), u"|embebido usuario=%s" % (users[usuarioactual.lower()]), wtext)
            newtext = re.sub(ur"(?im)\|autor={{bambuser channel\|%s}}" % (usuarioactual.lower()), u"|autor={{bambuser channel|%s}}" % (users[usuarioactual.lower()]), newtext)
            page.put(newtext, u"BOT - Corrigiendo nombre")
            newtitle = re.sub(ur"%s" % (re.sub(ur"[\+\_]", ur" ", usuarioactual.lower())), ur"%s" % (users[usuarioactual.lower()]), wtitle)
            page.move(newtitle, reason=u"BOT - Corrigiendo nombre", leaveRedirect=False)

if __name__ == '__main__':
    main()
