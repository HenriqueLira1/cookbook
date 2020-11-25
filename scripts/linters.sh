#! /usr/bin/env bash
set -e

ROOT="./src"
BANDIT_CONFIG="bandit.yaml"

DOCKER_NODEPS="docker-compose run --no-deps cookbook"
DOCKER="docker-compose run cookbook"

function print_header() {
    YELLOW='\033[1;33m'
    NC='\033[0m'
    MSG="$1"

    echo -e "\n${YELLOW}* ${MSG}${NC}"
}

print_header "BLACK"
$DOCKER_NODEPS black --check $ROOT

print_header "ISORT"
$DOCKER_NODEPS isort --check $ROOT

print_header "FLAKE8"
$DOCKER_NODEPS flake8 $ROOT

print_header "BANDIT"
$DOCKER_NODEPS bandit -r $ROOT -c $BANDIT_CONFIG

print_header "MIGRATION LINTER"
$DOCKER python src/manage.py lintmigrations

print_header "GENERAL CHECK"
$DOCKER_NODEPS python src/manage.py check --deploy
