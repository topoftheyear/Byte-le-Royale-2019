#!/bin/bash

# trap ctrl-c and call ctrl_c()
trap ctrl_c INT

function ctrl_c() {
    kill $p1;
    kill $p2;
}

echo "Starting Server..."
python -m game.scripts.server --server-verbose &
p1=$!

sleep 6;

echo "Starting Client..."
python -m game.scripts.client --client-verbose &
p2=$!

wait $p1 $p2;
exit;
