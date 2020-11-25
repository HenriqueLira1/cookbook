#! /usr/bin/env bash

YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}* Installing requirements-dev.txt${NC}"
pip install -r requirements-dev.txt

echo -e "${YELLOW}* Installing pre-commit${NC}"
pre-commit install --config .pre-commit-config.yaml

echo -e "${YELLOW}* Setting up .env.dev${NC}"
echo -e "${YELLOW}* WARNING: You still need to add the VARIABLES${NC}"
cp .env.dev
