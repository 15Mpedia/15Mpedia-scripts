#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2011-2015 emijrp <emijrp@gmail.com>
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

#This script generates redirects for wiki articles
#removing uppercase, accents and other symbols

import re
import sys
import time

import pywikibot
import pywikibot.pagegenerators as pagegenerators
import unicodedata

def removeaccute(s):
    return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))

def remove1(s): #replace with no-space
    s = re.sub(ur"[\.\:\;\,\"\!\¡\«\»]", ur"", s)
    return s

def remove2(s): #replace with a single space
    s = re.sub(ur"[\-\–]", ur" ", s)
    return s

def unquote(s):
    s = re.sub(ur"&#34;", ur'"', s)
    return s

def main():
    skip = u''
    if len(sys.argv) > 1:
        site = pywikibot.Site(sys.argv[1], sys.argv[1])
    else:
        print 'python script.py wikifamily [skiptopage]'
        sys.exit()
    if len(sys.argv) > 2:
        skip = sys.argv[2]
    gen = pagegenerators.AllpagesPageGenerator(start=skip, namespace=0, site=site)
    pre = pagegenerators.PreloadingGenerator(gen, pageNumber=250)
    alltitles = []
    c = 0
    for page in pre:
        if not page.exists(): #do not put .isRedirectPage() or it will never find redirects when checking below before creating
            continue
        alltitles.append(page.title())
        print page.title()
        c +=1
        if c % 250 == 0:
            time.sleep(1)
        
    for wtitle in alltitles:
        if wtitle.startswith('Lista de votaciones') or \
            wtitle.startswith('Votaciones'):
            continue
        
        if len(wtitle) > 1:
            wtitle_ = wtitle[0]+wtitle[1:].lower()
            redirects = set()
            for t in [wtitle, wtitle_]:
                redirects.add(t)
                redirects.add(remove1(t))
                redirects.add(remove2(t))
                redirects.add(removeaccute(t))
                redirects.add(remove1(remove2(t)))
                redirects.add(remove1(removeaccute(t)))
                redirects.add(remove2(removeaccute(t)))
                redirects.add(remove1(remove2(removeaccute(t))))
                
                #redirects para Lista de ...
                if wtitle.startswith('Lista de ') and len(wtitle)>10:
                    listade = wtitle[9:]
                    listade = listade[0].upper()+listade[1:]
                    redirects.add(listade)
                
                #redirects para Lista de acampadas/asambleas/... de/del/de la Madrid/provincia de Madrid
                if sys.argv[1].lower() == '15mpedia':
                    #preposiciones en/de para listas de colectivos
                    for colectivo in [u'acampadas', u'asambleas', u'bancos de tiempo', u'centros sociales', u'CSOA', u'CSO', u'comedores sociales']:
                        #!!!no incluir asociaciones, ni comisiones, ni manifestaciones, ni medios, ni plataformas porque detrás del "de " puede venir un tema y no un lugar
                        if wtitle.startswith('Lista de %s de ' % colectivo):
                            redirects.add(re.sub(ur"Lista de %s de " % colectivo, ur"Lista de %s en " % colectivo, wtitle))
                        elif wtitle.startswith('Lista de %s del ' % colectivo):
                            redirects.add(re.sub(ur"Lista de %s del " % colectivo, ur"Lista de %s en el " % colectivo, wtitle))
                        elif wtitle.startswith('Lista de %s de la ' % colectivo):
                            redirects.add(re.sub(ur"Lista de %s de la " % colectivo, ur"Lista de %s en la " % colectivo, wtitle))
                    
                    #sinonimos para listas de comedores sociales, centros sociales y medios de comunicación
                    if wtitle.startswith(u'Lista de bancos de tiempo ') and len(wtitle)>30:
                        redirects.add(re.sub(ur"Lista de bancos de tiempo ", ur"Lista de BdT ", wtitle))
                    elif wtitle.startswith(u'Lista de comedores sociales ') and len(wtitle)>30:
                        redirects.add(re.sub(ur"Lista de comedores sociales ", ur"Lista de comedores ", wtitle))
                    elif wtitle.startswith(u'Lista de centros sociales ') and len(wtitle)>30:
                        redirects.add(re.sub(ur"Lista de centros sociales ", ur"Lista de CSOA ", wtitle))
                        redirects.add(re.sub(ur"Lista de centros sociales ", ur"Lista de CSO ", wtitle))
                    elif wtitle.startswith(u'Lista de medios de comunicación ') and len(wtitle)>40:
                        redirects.add(re.sub(ur"Lista de medios de comunicación ", ur"Lista de medios ", wtitle))
                    elif wtitle.startswith(u'Lista de círculos de Podemos ') and len(wtitle)>40:
                        redirects.add(re.sub(ur"Lista de círculos de Podemos ", ur"Lista de nodos de Podemos ", wtitle))
                    
                    #gentilicios para ccaa
                    #solo los que no sean ambiguos, ej: Andalucía. Ej ambiguos: Madrileños (pq abarcaría ccaa, prov, municipio)
                    #división entre feminimo y masculino
                    for xccaa, xfem, xmas in [[u"Andalucía", u"andaluzas", u"andaluces"], [u"Extremadura", u"extremeñas", u"extremeños"], ]:
                        if re.search(ur"(?im)^Lista de (acampadas|asambleas) (de|en) %s$" % (xccaa), wtitle):
                            redirects.add(re.sub(ur"(?im)^Lista de (acampadas|asambleas) (de|en) %s$" % (xccaa), ur"Lista de \1 %s" % (xfem), wtitle))
                        if re.search(ur"(?im)^Lista de (bancos de tiempo|centros sociales|CSOA|CSO|comedores sociales) (de|en) %s$" % (xccaa), wtitle):
                            redirects.add(re.sub(ur"(?im)^Lista de (bancos de tiempo|centros sociales|CSOA|CSO|comedores sociales) (de|en) %s$" % (xccaa), ur"Lista de \1 %s" % (xmas), wtitle))
                    
                    #fosas comunes
                    if wtitle.startswith(u'Lista de fosas en '):
                        redirects.add(re.sub(ur"Lista de fosas en ", ur"Lista de fosas comunes en ", wtitle))
                        redirects.add(re.sub(ur"Lista de fosas en ", ur"Lista de fosas de ", wtitle))
                        redirects.add(re.sub(ur"Lista de fosas en ", ur"Lista de fosas comunes de ", wtitle))
                    
                    #asesinatos machistas
                    if wtitle.startswith(u'Lista de asesinatos machistas en '):
                        redirects.add(re.sub(ur"Lista de asesinatos machistas en ", ur"Lista de asesinadas en ", wtitle))
                        redirects.add(re.sub(ur"Lista de asesinatos machistas en ", ur"Lista de mujeres asesinadas en ", wtitle))
                        redirects.add(re.sub(ur"Lista de asesinatos machistas en ", ur"Lista de mujeres muertas por violencia de género en ", wtitle))
                        redirects.add(re.sub(ur"Lista de asesinatos machistas en ", ur"Lista de mujeres muertas por violencia machista en ", wtitle))
                        redirects.add(re.sub(ur"Lista de asesinatos machistas en ", ur"Lista de muertes relacionadas con violencia machista en ", wtitle))
                        redirects.add(re.sub(ur"Lista de asesinatos machistas en ", ur"Lista de asesinatos relacionados con violencia machista en ", wtitle))
                        redirects.add(re.sub(ur"Lista de asesinatos machistas en ", ur"Lista de muertes por violencia machista en ", wtitle))
                        redirects.add(re.sub(ur"Lista de asesinatos machistas en ", ur"Lista de asesinatos por violencia de género en ", wtitle))
                        redirects.add(re.sub(ur"Lista de asesinatos machistas en ", ur"Lista de asesinatos por violencia machista en ", wtitle))
                    
                    #actualidad
                    if wtitle.startswith(u'Actualidad en '):
                        redirects.add(re.sub(ur"Actualidad en ", ur"Actualidad de ", wtitle))
                    
                    #capitalismo
                    if wtitle.startswith(u'Crímenes del capitalismo '):
                        redirects.add(re.sub(ur"Crímenes del capitalismo ", ur"Crímenes capitalistas ", wtitle))
                    
                    if wtitle.endswith(u' regímenes capitalistas'):
                        redirects.add(re.sub(ur" regímenes capitalistas", ur" el capitalismo", wtitle))
                        redirects.add(re.sub(ur" regímenes capitalistas", ur" estados capitalistas", wtitle))
                        redirects.add(re.sub(ur" regímenes capitalistas", ur" países capitalistas", wtitle))
                    
                    if wtitle.endswith(u' el capitalismo'):
                        redirects.add(re.sub(ur" el capitalismo", ur" regímenes capitalistas", wtitle))
                        redirects.add(re.sub(ur" el capitalismo", ur" estados capitalistas", wtitle))
                        redirects.add(re.sub(ur" el capitalismo", ur" países capitalistas", wtitle))
                    
                    #memoria historica
                    if wtitle.startswith(u'Memoria histórica en '):
                        redirects.add(re.sub(ur"Memoria histórica en ", ur"Memoria Histórica en ", wtitle))
                        redirects.add(re.sub(ur"Memoria histórica en ", ur"Memoria histórica de ", wtitle))
                        redirects.add(re.sub(ur"Memoria histórica en ", ur"Memoria Histórica de ", wtitle))
                        redirects.add(re.sub(ur"Memoria histórica en ", ur"Memoria de ", wtitle))
                        redirects.add(re.sub(ur"Memoria histórica en ", ur"Memoria en ", wtitle))
                        redirects.add(re.sub(ur"Memoria histórica en ", ur"MH de ", wtitle))
                        redirects.add(re.sub(ur"Memoria histórica en ", ur"MH en ", wtitle))
                    
                    if wtitle.startswith(u'Lista de personas fusiladas por el franquismo en '):
                        redirects.add(re.sub(ur"Lista de personas fusiladas por el franquismo en ", ur"Lista de fusilados por el franquismo en ", wtitle))
                        redirects.add(re.sub(ur"Lista de personas fusiladas por el franquismo en ", ur"Fusilados en ", wtitle))
                        redirects.add(re.sub(ur"Lista de personas fusiladas por el franquismo en ", ur"Fusilamientos en ", wtitle))
                        redirects.add(re.sub(ur"Lista de personas fusiladas por el franquismo en ", ur"Asesinados por el franquismo en ", wtitle))
                    
                    if wtitle.startswith(u'Lista de víctimas españolas del nazismo deportadas al Campo de concentración de '):
                        redirects.add(re.sub(ur"Lista de víctimas españolas del nazismo deportadas al Campo de concentración de ", ur"Deportados a ", wtitle))
                        redirects.add(re.sub(ur"Lista de víctimas españolas del nazismo deportadas al Campo de concentración de ", ur"Personas deportadas a ", wtitle))
                        redirects.add(re.sub(ur"Lista de víctimas españolas del nazismo deportadas al ", ur"Deportados al ", wtitle))
                        redirects.add(re.sub(ur"Lista de víctimas españolas del nazismo deportadas al ", ur"Personas deportadas al ", wtitle))
                        redirects.add(re.sub(ur"Lista de víctimas españolas del nazismo deportadas al ", ur"Víctimas del ", wtitle))
                    
                    #propaganda
                    if wtitle.startswith(u'Manipulación y propaganda '):
                        redirects.add(re.sub(ur"Manipulación y propaganda ", ur"Manipulación ", wtitle))
                        redirects.add(re.sub(ur"Manipulación y propaganda ", ur"Propaganda ", wtitle))
                        redirects.add(re.sub(ur"Manipulación y propaganda ", ur"Propaganda y manipulación ", wtitle))
                    
                    #violencia de género
                    if wtitle.startswith(u'Violencia de género en '):
                        redirects.add(re.sub(ur"Violencia de género en ", ur"Violencia intrafamiliar en ", wtitle))
                        redirects.add(re.sub(ur"Violencia de género en ", ur"Violencia contra la mujer en ", wtitle))
                        redirects.add(re.sub(ur"Violencia de género en ", ur"Violencia contra las mujeres en ", wtitle))
                        redirects.add(re.sub(ur"Violencia de género en ", ur"Violencia machista en ", wtitle))
                        redirects.add(re.sub(ur"Violencia de género en ", ur"Violencia de sexo en ", wtitle))
                        redirects.add(re.sub(ur"Violencia de género en ", ur"Violencia familiar en ", wtitle))
                        redirects.add(re.sub(ur"Violencia de género en ", ur"Violencia doméstica en ", wtitle))
                    
            print redirects
            for redirect in redirects:
                redirect = redirect.strip()
                if redirect and redirect != wtitle and not redirect in alltitles:
                    red = pywikibot.Page(site, redirect)
                    if not red.exists():
                        output = u"#REDIRECT [[%s]]" % (wtitle)
                        msg = u"BOT - Creating redirect to [[%s]]" % (wtitle)
                        red.text = output
                        red.save(msg)
                        time.sleep(0.1)

if __name__ == '__main__':
    main()
