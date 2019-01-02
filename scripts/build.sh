#!/bin/bash

rm *.pyz; 

rm -rf wrapper/game
python3 -m zipapp wrapper -c -p "/usr/bin/env python3" -o br_launcher.pyz; 
rm -rf wrapper/game

