#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2014 emijrp
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

import re
import time
import urllib
import urllib2

def main():
    tags = ['acampadasol', 'spanishrevolution', 'acampadabcn', 'acampadasevilla', 'acampadavalencia', 'marchasdeladignidad', 'mareablanca', 'mareaverde', 'mareavioleta', 'juventudsinfuturo'] #'democraciarealya']
    for tag in tags:
        page = 1
        while True:
            url = 'http://vimeo.com/tag:%s/page:%d/sort:date/format:thumbnail' % (tag, page)
            #print url
            try:
                req = urllib2.Request(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:10.0) Gecko/20100101 Firefox/10.0 (Chrome)'})
                raw = unicode(urllib2.urlopen(req).read(), 'utf-8')
            except:
                print 'Error al leer', url
                break
            ids = re.findall(ur'<li (?:class="last" )?id="clip_(\d+)"', raw)
            if ids:
                for id in ids:
                    print id
            else:
                break
            page += 1
            time.sleep(3)

if __name__ == '__main__':
    main()

