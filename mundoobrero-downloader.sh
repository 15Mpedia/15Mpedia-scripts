#!/bin/bash

for i in {1..1000}
do
    wget -c --user-agent="Mozilla/5.0" "http://www.mundoobrero.es/pl.php?id=$i" -O "mundoobrero-$i.html"
    sleep 2
done
