#!/bin/bash

set -x

cd /code

echo "Generating game_data.json"
./br_launcher.pyz generate

echo "Starting server"
./br_launcher.pyz \
    server \
    --port 8888 \
    --connection-wait-timer 10 \
    --wait-timeout 10 \
    --no-wait \
    --game-length 2000

