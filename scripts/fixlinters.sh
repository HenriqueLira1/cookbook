#! /usr/bin/env bash
# shellcheck disable=SC2086
set -e

function print_header() {
    YELLOW='\033[1;33m'
    NC='\033[0m'
    MSG="$1"

    echo -e "\n${YELLOW}* ${MSG}${NC}"
}

ROOT="./src"
LOCAL="docker-compose run --no-deps cookbook"

# insert -l argument to run on your local machine
while (( "$#" ))
do
    if [ "$1" == "-l" ]; then
        LOCAL=""
    fi
    shift
done

print_header "BLACK"
$LOCAL black $ROOT

print_header "ISORT"
$LOCAL isort $ROOT

print_header "FLAKE8"
$LOCAL flake8 $ROOT
