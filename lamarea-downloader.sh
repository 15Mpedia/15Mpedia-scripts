#!/bin/bash

for i in {1..45}
do
    wget -c --user-agent="Mozilla/5.0" "http://www.lamarea.com/secciones/internacional/page/$i/" -O "lamarea-int-$i.html"
    sleep 2
done
