#!/bin/bash

if [ -z $1 ]; then
    port_no=8080
else
    port_no=$1
fi

echo "Port number: $port_no";


# trap ctrl-c and call ctrl_c()
trap ctrl_c INT

function ctrl_c() {
    kill $p1;
    kill $p2;
}

echo "Starting Server..."
python -m game.scripts.server --port $port_no &
p1=$!

sleep 6;

echo "Starting Client..."
if python -m game.scripts.client --port $port_no; then
    echo "$?";
    echo "Client exited peacfully, waiting for server to close.";

    wait $p1

else
    # script died
    echo "$?";
    echo "Client exited with error, giving server a chance to close."
    sleep 1;

    # if server is still running kill it
    echo "Killing Server."
    kill $p1

    rm results.json;
fi


# sleep

echo "Run finished. EXITING."

exit;
