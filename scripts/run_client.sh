#!/bin/bash

cd /code

./br_launcher.pyz \
    client \
    --port 8888 \
    --host br_server

exit $?
