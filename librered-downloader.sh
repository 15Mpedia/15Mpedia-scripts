#!/bin/bash

for i in {1000..1999}
do
    wget -c --user-agent="Mozilla/5.0" "http://www.librered.net/?p=$i" -O "librered-$i.html"
    sleep 2
done
