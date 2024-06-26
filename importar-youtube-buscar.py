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

import os
import random
import re
import subprocess
import sys
import time
import urllib
import urllib2
import pywikibot

def main():
    # Cargar videos ya indexados en el wiki
    videosuploaded = []
    startid = '-'
    while startid:
        print 'Leyendo videos indexados desde %s' % (startid)
        queryurl = 'http://15mpedia.org/w/index.php?title=Especial%%3AAsk&q=[[Page+has+default+form%%3A%%3AArchivo]][[Embebido%%3A%%3AYouTube]][[Embebido+id%%3A%%3A%%3E%s]]&po=%%3FEmbebido+id%%0D%%0A&eq=yes&p[format]=broadtable&sort_num=&order_num=ASC&p[limit]=1000&p[offset]=&p[link]=all&p[sort]=embebido+id&p[headers]=show&p[mainlabel]=-&p[intro]=&p[outro]=&p[searchlabel]=%%26hellip%%3B+siguientes+resultados&p[default]=&p[class]=sortable+wikitable+smwtable&eq=yes' % (startid)
        f = urllib.urlopen(queryurl)
        html = unicode(f.read(), 'utf-8')
        #print html
        m = re.findall(ur'(?im)<td class="Embebido-id">([^<>]+?)</td>', html)
        if len(m) > 1:
            startid = m[-1]
            videosuploaded += m
        elif len(m) == 1:
            startid = ''
            videosuploaded.append(m[0])
        else:
            print 'La regexp fallo'
            sys.exit()
    
    videosuploaded = list(set(videosuploaded))
    videosuploaded.sort()
    print 'En el wiki hay %d videos indexados' % (len(videosuploaded))
    
    # Cargar los que han sido seleccionados para subir
    videostoupload = []
    page = pywikibot.Page(pywikibot.Site('15mpedia', '15mpedia'), u'15Mpedia:Importar YouTube/Por importar')
    videostoupload = re.findall(ur'(?im)\|por importar=([^\n]+)\n', page.text)[0].split(', ')
    videostoupload = list(set(videostoupload))
    videostoupload.sort()
    '' in videostoupload and videostoupload.remove('')
    print 'Hay %d videos por importar' % (len(videostoupload))
    #print videostoupload
    
    # Retirar los que ya han sido subidos
    videostoupload2 = videostoupload
    c = 0
    for x in videostoupload2:
        if x in videosuploaded:
            videostoupload.remove(x)
            c += 1
    videostoupload.sort()
    print 'Retirando %d videos que ya han sido importados' % (c)
    if c > 0:
        page.text = re.sub(ur'(?im)(\|\s*por importar\s*=\s*[^\n]+)\n', ur'|por importar=%s\n' % (', '.join(videostoupload)), page.text)
        page.save(u'BOT - Ordenando lista y retirando los que ya han sido subidos')
    
    # Cargar los que han sido excluidos
    videosexcluded = []
    page = pywikibot.Page(pywikibot.Site('15mpedia', '15mpedia'), u'15Mpedia:Importar YouTube/Excluidos')
    videosexcluded = re.findall(ur'\|excluidos=(.*)', page.text)[0].split(', ')
    videosexcluded = list(set(videosexcluded))
    '' in videosexcluded and videosexcluded.remove('')
    print 'Hay %d videos excluidos' % (len(videosexcluded))
    #print videosexcluded
    
    # Retirar de la pagina de analisis aquellos que ya han sido analizados
    page = pywikibot.Page(pywikibot.Site('15mpedia', '15mpedia'), u'15Mpedia:Importar YouTube')
    text = page.text
    m = re.findall(ur'(?im)(\{\{\s*Importar YouTube vídeo\s*\|\s*id=\s*[^\|]+\s*\|\s*título\s*=\s*[^\}]+\s*\}\})', text)
    newtext = page.text
    importarnum = 0
    excluirnum = 0
    for i in m:
        #print i
        videoid = re.findall(ur'\|\s*id\s*=\s*([^\s]+)\s*', i)[0]
        if videoid in videostoupload:
            print 'El video %s ha sido marcado para subir' % (videoid)
            newtext = newtext.replace(i, '')
            importarnum += 1
        elif videoid in videosexcluded:
            print 'El video %s ha sido marcado para excluir' % (videoid)
            newtext = newtext.replace(i, '')
            excluirnum += 1
    if text != newtext:
        print 'Retirando %d vídeos analizados: %d para importar, %d para excluir' % (importarnum + excluirnum, importarnum, excluirnum)
        page.text = newtext
        page.save(u'BOT - Retirando %d vídeos analizados: %d para importar, %d para excluir' % (importarnum + excluirnum, importarnum, excluirnum))
    
    # Cargar las opciones de configuracion
    print 'Cargando opciones de configuracion'
    page = pywikibot.Page(pywikibot.Site('15mpedia', '15mpedia'), u'15Mpedia:Importar YouTube')
    text = page.text
    m = re.findall(ur'(?im)(\{\{\s*Importar YouTube vídeo\s*\|\s*id=\s*[^\|]+\s*\|\s*título\s*=\s*[^\}]+\s*\}\})', text)
    videosinpage = len(m)
    maxvideos = 100
    if re.findall(ur'(?im)\|\s*límite\s*=([\d]+)', text):
        maxvideos = int(re.findall(ur'(?im)\|\s*límite\s*=\s*([\d]+)', text)[0].strip())
    print 'Limite de videos es %d' % (maxvideos)
    keywords = ['acampadasol']
    if re.findall(ur'(?im)\|\s*palabras clave\s*=([^\n\|]+)', text):
        keywords = [x.strip() for x in re.findall(ur'(?im)\|\s*palabras clave\s*=([^\n\|]+)', text)[0].strip().split(', ')]
        '' in keywords and keywords.remove('')
    print 'Encontradas %d palabras clave: %s' % (len(keywords), ', '.join(keywords))
    orden = 'Ninguno'
    if re.findall(ur'(?im)\|\s*órden\s*=([^\n\|]+)', text):
        orden = re.findall(ur'(?im)\|\s*órden\s*=([^\n\|]+)', text)[0].strip()
    print 'Orden es %s' % (orden)
    if orden == 'Aleatorio':
        random.shuffle(keywords)
    elif orden == 'Alfabético':
        keywords.sort()
    
    if videosinpage >= maxvideos:
        print 'No hace falta agregar mas videos, ya hay %d' % (videosinpage)
        sys.exit()
    
    # Buscar nuevos candidatos
    videos = {}
    maxpages = 10
    for keyword in keywords:
        if videosinpage + len(videos.keys()) >= maxvideos:
            break
        print '\n', '#'*40, '\n', ' Analizando keyword', keyword, '\n', '#'*40
        salir = False
        for page in range(1, maxpages):
            if videosinpage + len(videos.keys()) >= maxvideos:
                print 'Alcanzado el limite de %d videos, no hace falta buscar mas candidatos' % (maxvideos)
                break
            print '\nPagina', page, '\n', '-'*40
            searchurl = 'https://www.youtube.com/results?search_query=%%22%s%%22&lclk=video&filters=video&page=%d' % (keyword, page)
            output = unicode(subprocess.Popen(["./youtube-dl", searchurl, "--get-id", "--get-title"], stdout=subprocess.PIPE).communicate()[0].strip(), 'utf-8')
            lines = output.splitlines()
            #print output
            if len(lines) % 2 != 0:
                print 'Error, se necesita un numero par de lineas'
                break
            c = 0
            while c < len(lines)-1:
                videotitle = lines[c]
                videoid = lines[c+1]
                if not videoid in videosuploaded and \
                   not videoid in videostoupload and \
                   not videoid in videosexcluded and \
                   not videoid in text and \
                   not videoid in videos.keys():
                    print len(videos.keys()), videoid, videotitle
                    videos[videoid] = videotitle
                c += 2
    
    #print videos.items()
    print 'La busqueda ha devuelto %d videos' % (len(videos.items()))
    
    # Agregar hasta llegar al maximo
    page = pywikibot.Page(pywikibot.Site('15mpedia', '15mpedia'), u'15Mpedia:Importar YouTube')
    text = page.text
    
    videosplain = u''
    c = 0
    for videoid, videotitle in videos.items():
        if videosinpage + c >= maxvideos:
            break
        videotitle = re.sub(ur'[\[\]]', u'', videotitle)
        videosplain += u'{{Importar YouTube vídeo\n|id=%s\n|título=%s\n}}' % (videoid, videotitle)
        c += 1
    
    print 'Se agregaran %d videos' % (c)
    
    newtext = u'%s|vídeos=%s%s' % (text.split(u'|vídeos=')[0], videosplain, text.split(u'|vídeos=')[1])
    if text != newtext:
        page.text = newtext
        page.save(u'BOT - Añadiendo %d vídeos para analizar' % (c))

if __name__ == '__main__':
    main()
