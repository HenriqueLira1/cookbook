#! /usr/bin/env bash
# shellcheck disable=SC2086
set -e

LOCAL="docker-compose run --no-deps cookbook"
COMMAND="pytest"
TESTPATH="./src/tests/unit"
ARGS="--cov=src --cov-report=term:skip-covered"

while (( "$#" ))
do
    if [ "$1" == "-l" ]; then
        LOCAL=""
    elif [ "$1" == "--include-integration" ]; then
        TESTPATH="./src/tests"
    elif [ "$1" == "-s" ]; then
        ARGS="-s --show-capture=all $ARGS"
    else
        ARGS="$1 $ARGS"
    fi

    shift
done

echo "* RUNNING COVERAGE AND TESTS"
$LOCAL $COMMAND $TESTPATH $ARGS
