#!/bin/bash

rm -rf scenarios;
mkdir scenarios;

for (( i=0; i<50; i++ )) do
    echo "Generation Scenario $i"
    python -m game.scripts.generate;
    cp game_data.json scenarios/$i.json;
done;

