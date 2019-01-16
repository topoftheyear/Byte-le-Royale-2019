#!/bin/bash

cd /code

./br_launcher.pyz \
    client \
    --port 8888 \
    --host bl_server
    --wait-timeout 600

exit $?
