#! /usr/bin/env bash

YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}* Creating venv${NC}"
python3 -m venv .venv

echo -e "${YELLOW}DONE! Now you can use it by running: 'source .venv/bin/activate'${NC}"
