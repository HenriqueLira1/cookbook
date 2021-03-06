#! /usr/bin/env bash
# shellcheck disable=SC2086
set -e

LOCAL="docker-compose run cookbook"
COMMAND="pytest"
ARGS="./src/tests/integration"

while (( "$#" ))
do
    if [ "$1" == "-s" ]; then
        ARGS="$ARGS -s --show-capture=all $ARGS"
    else
        ARGS="$ARGS $1"
    fi

    shift
done

echo "* RUNNING TESTS"
$LOCAL $COMMAND $ARGS
