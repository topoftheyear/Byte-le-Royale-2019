#!/bin/bash

rm *.pyz; 

cp -rf game wrapper/
python3 -m zipapp wrapper -p "/usr/bin/env python3" -o br_launcher.pyz; 
rm -rf wrapper/game

