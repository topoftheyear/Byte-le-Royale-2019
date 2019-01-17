#!/bin/bash

cd /code

echo "Generating game_data.json"
./br_launcher.pyz generate

echo "Starting server"
./br_launcher.pyz \
    server \
    --port 8888 \
    --no-wait \
    --connection-wait-timer 10 \
    --wait-timeout 10

echo '{
    "leaderboard": [
        {
            "team_name": "herp derp",
            "credits": 1000
        },
        {
            "team_name": "team 2",
            "credits": 999
        }
    ],
    "accolades": {
        "badass": "herp derp"
    }
}' > results.json
