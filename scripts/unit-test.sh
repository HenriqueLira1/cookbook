#! /usr/bin/env bash
set -e

LOCAL="docker-compose run --no-deps cookbook"
COMMAND="pytest"
ARGS="./src/tests/unit"

while (( "$#" ))
do
    if [ "$1" == "-l" ]; then
        LOCAL=""
    elif [ "$1" == "-s" ]; then
        ARGS="$ARGS -s --show-capture=all $ARGS"
    else
        ARGS="$ARGS $1"
    fi

    shift
done

echo "* RUNNING TESTS"
$LOCAL $COMMAND $ARGS
