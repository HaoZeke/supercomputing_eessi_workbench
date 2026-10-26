#!/bin/bash
# Predict commands from the data-movement deck, 26 October 2026.
# Run this from an empty directory on scratch. Write down the real time.
set -eu
mkdir -p src out
yes data | head -n 20000 | split -l 1 -a 5 -d - src/f
ls src | wc -l
{ time cp -r src out/by-cp; }
tar --sort=name -cf src.tar src
{ time cp src.tar out/; }
{ time rsync -a src/ out/by-rsync/; }
sha256sum src.tar > src.tar.sha256
cp src.tar.sha256 out/
( cd out && sha256sum -c src.tar.sha256 )
