#!/bin/bash

set -e

printf "\n\n"
echo "Build";
./scripts/build.sh; 
printf "\n\n"
echo "Generate";
./br_launcher.pyz generate; 
printf "\n\n"
echo "Run";
./br_launcher.pyz run $@; 
printf "\n\n"
echo "Visualizer";
./br_launcher.pyz visualizer --team-name Derp
