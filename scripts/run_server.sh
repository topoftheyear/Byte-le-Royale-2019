#!/bin/bash

cd /code

echo "Generating game_data.json"
./br_launcher.pyz generate

echo "Starting server"
./br_launcher.pyz \
    server \
    --port 8888 \
    --no-wait \
    --connection-wait-timer 120 \
    --wait-timeout 600
