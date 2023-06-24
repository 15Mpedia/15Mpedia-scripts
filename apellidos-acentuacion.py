#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2023 emijrp <emijrp@gmail.com>
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
import sys
import urllib.parse
import urllib.request
import pywikibot
import pywikibot.pagegenerators as pagegenerators
import unicodedata

def removeaccute(s):
    return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))

def bestcandidate(x, l):
    occurences = {}
    for word in l:
        if word in occurences.keys():
            occurences[word] += 1
        else:
            occurences[word] = 1
    occurenceslist = [[freq, word] for word, freq in occurences.items()]
    occurenceslist.sort(reverse=True)
    totalfreq = len(l)
    
    best = occurenceslist[0][1] #coger el más usado por defecto, menos si...
    if len(occurenceslist) == 1: #todos los candidatos son iguales
        if occurenceslist[0][1]: #no es vacio
            best = occurenceslist[0][1]
    elif re.search(r'(?im)[áéíóúü]', '-'.join(l)) and sum([freq for freq, word in occurenceslist])>=10: #si hay alguno con acentos
        #el que represente el >25% de las ocurrencias si hay >=10 ocurrencias en total
        for freq, word in occurenceslist:
            if re.search(r'(?im)[áéíóúü]', word) and freq > totalfreq/4.0: #25% y con acentos, ok
                best = word
                break
    else:
        best = "NOCONCLUYENTE"
    
    return best

def main():
    site = pywikibot.Site('15mpedia', '15mpedia')
    catnames = [
        'Categoría:Personas fusiladas por el franquismo', 
        'Categoría:Víctimas del nazismo', 
    ]
    acentos = {}
    start = ''
    generatelist = False
    replacements = {}
    if generatelist:
        for catname in catnames:
            category = pywikibot.Category(site, catname)
            gen = pagegenerators.CategorizedPageGenerator(category=category, start=start, namespaces=[0])
            pre = pagegenerators.PreloadingGenerator(gen, pageNumber=250)
            """templatepage = pywikibot.Page(site, template)
            gen = pagegenerators.ReferringPageGenerator(templatepage, followRedirects=True, withTemplateInclusion=True)
            pre = pagegenerators.PreloadingGenerator(gen, pageNumber=50)"""
            
            c = 0
            for page in pre:
                if not page.exists() or page.isRedirectPage():
                    continue
                wtext = page.text
                wtitle = page.title()
                if not re.search(r'{{Infobox Persona', wtext):
                    continue
                print('\n== %s ==' % (wtitle))
                
                try:
                    nombre = re.findall(r'(?im)\|nombre=([^\|]*)', wtext)[0].strip()
                    primerapellido = re.findall(r'(?im)\|primer apellido=([^\|]*)', wtext)[0].strip()
                    segundoapellido = re.findall(r'(?im)\|segundo apellido=([^\|]*)', wtext)[0].strip()
                except:
                    continue
                
                if re.search(r'(?im)[^a-záéíóúü]', nombre+primerapellido+segundoapellido) or len(nombre) <= 3 or len(primerapellido) <= 3 or len(segundoapellido) <= 3:
                    continue
                
                print(nombre, primerapellido, segundoapellido)
                nombrerem = removeaccute(nombre).lower()
                primerapellidorem = removeaccute(primerapellido).lower()
                segundoapellidorem = removeaccute(segundoapellido).lower()
                
                if nombrerem:
                    if nombrerem in acentos.keys():
                        acentos[nombrerem].append(nombre)
                    else:
                        acentos[nombrerem] = [nombre]
                if primerapellidorem:
                    if primerapellidorem in acentos.keys():
                        acentos[primerapellidorem].append(primerapellido)
                    else:
                        acentos[primerapellidorem] = [primerapellido]
                if segundoapellidorem:
                    if segundoapellidorem in acentos.keys():
                        acentos[segundoapellidorem].append(segundoapellido)
                    else:
                        acentos[segundoapellidorem] = [segundoapellido]
                
                #c += 1
                #if c > 5000:
                #    break
        
        acentoslist = [[x, l] for x, l in acentos.items()]
        acentoslist.sort()
        output = ""
        for x, l in acentoslist:
            best = bestcandidate(x, l)
            if len(l) >= 10 and re.search(r'(?im)[áéíóúü]', best):
                output += "\n# [[%s]]->[[%s]]" % (x, best)
                replacements[x] = best
        
        page = pywikibot.Page(pywikibot.Site('15mpedia', '15mpedia'), "Usuario:Emijrp/Lista de apellidos (acentuación)")
        page.text = output
        page.save('BOT - Actualizando lista', botflag=True)
    else:
        page = pywikibot.Page(pywikibot.Site('15mpedia', '15mpedia'), "Usuario:Emijrp/Lista de apellidos (acentuación)")
        wtext = page.text
        m = re.findall(r"(?im)\[\[([^\[\]]+)\]\]\s*->\s*\[\[([^\[\]]+)\]\]", wtext)
        for x, y in m:
            replacements[x] = y
    
    #replacements
    start = ''
    for catname in catnames:
        category = pywikibot.Category(site, catname)
        gen = pagegenerators.CategorizedPageGenerator(category=category, start=start, namespaces=[0])
        pre = pagegenerators.PreloadingGenerator(gen, pageNumber=250)
        
        for page in pre:
            if not page.exists() or page.isRedirectPage():
                continue
            wtext = page.text
            wtitle = page.title()
            nombrecompletooriginal = wtitle
            if not re.search(r'{{Infobox Persona', wtext):
                continue
            print('\n== %s ==' % (wtitle))
            
            try:
                nombre = re.findall(r'(?im)\|nombre=([^\|]*)', wtext)[0].strip()
                primerapellido = re.findall(r'(?im)\|primer apellido=([^\|]*)', wtext)[0].strip()
                segundoapellido = re.findall(r'(?im)\|segundo apellido=([^\|]*)', wtext)[0].strip()
            except:
                continue
            
            if re.search(r'(?im)[^a-záéíóúü]', nombre+primerapellido+segundoapellido) or len(nombre) <= 3 or len(primerapellido) <= 3 or len(segundoapellido) <= 3:
                continue
            
            newtext = wtext
            nombrecompletobien = ""
            if not re.search(r'(?im)[^a-z]', nombre) and nombre.lower() in replacements.keys():
                newtext = re.sub(r"(?im)(\|nombre=)%s" % (nombre), r"\1%s" % (replacements[nombre.lower()]), newtext)
                newtext = re.sub(r"(?im)^%s" % (nombre), r"%s" % (replacements[nombre.lower()]), newtext)
                newtext = re.sub(r"(?im)^'''%s" % (nombre), r"'''%s" % (replacements[nombre.lower()]), newtext)
                nombrecompletobien += replacements[nombre.lower()]
            else:
                nombrecompletobien += nombre
            if not re.search(r'(?im)[^a-z]', primerapellido) and primerapellido.lower() in replacements.keys():
                newtext = re.sub(r"(?im)(\|primer apellido=)%s" % (primerapellido), r"\1%s" % (replacements[primerapellido.lower()]), newtext)
                newtext = re.sub(r"(?im)^('''[^ ]+) %s" % (primerapellido), r"\1 %s" % (replacements[primerapellido.lower()]), newtext)
                nombrecompletobien += " " + replacements[primerapellido.lower()]
            else:
                nombrecompletobien += " " + primerapellido
            if not re.search(r'(?im)[^a-z]', segundoapellido) and segundoapellido.lower() in replacements.keys():
                newtext = re.sub(r"(?im)(\|segundo apellido=)%s" % (segundoapellido), r"\1%s" % (replacements[segundoapellido.lower()]), newtext)
                newtext = re.sub(r"(?im)^('''[^ ]+ [^ ]+) %s" % (segundoapellido), r"\1 %s" % (replacements[segundoapellido.lower()]), newtext)
                nombrecompletobien += " " + replacements[segundoapellido.lower()]
            else:
                nombrecompletobien += " " + segundoapellido
            
            if wtext != newtext:
                pywikibot.showDiff(wtext, newtext)
                print("Trasladar a", nombrecompletobien)
                targetpage = pywikibot.Page(pywikibot.Site('15mpedia', '15mpedia'), nombrecompletobien)
                if targetpage.exists():
                    print("-->No se puede ya existe, saltamos")
                else:
                    print("Corrigiendo en el texto")
                    page.text = newtext
                    page.save("BOT - Corrigiendo acentos en el nombre: [[%s]]->[[%s]]" % (nombrecompletooriginal, nombrecompletobien), botflag=True)
                    print("Trasladando")
                    page.move(nombrecompletobien, reason="BOT - Trasladando tras corregir acentos en el nombre: [[%s]]->[[%s]]" % (nombrecompletooriginal, nombrecompletobien))
                    time.sleep(5)
                    originalpage = pywikibot.Page(pywikibot.Site('15mpedia', '15mpedia'), nombrecompletooriginal)
                    redirecttext = originalpage.text
                    originalpage.text = ""
                    print("Limpiando propiedades")
                    originalpage.save('BOT - Limpiando caché de propiedades semánticas', botflag=True)
                    time.sleep(5)
                    originalpage.text = redirecttext
                    print("Creamos redirect")
                    originalpage.save('BOT - Creando redirección hacia [[%s]]' % (nombrecompletobien), botflag=True)
                time.sleep(10)

if __name__ == '__main__':
    main()
