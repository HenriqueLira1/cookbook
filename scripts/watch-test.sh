#! /usr/bin/env bash
set -e

echo "* WATCHING TESTS"

docker-compose run cookbook ptw src --runner "pytest ./src --testmon"
