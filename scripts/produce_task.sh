#! /usr/bin/env bash
VALUE=$(cat "./scripts/payloads/task_sample.json")
RANDOM_ID=$(printf '%05d\n' $((1 + RANDOM % 100000000)))
VALUE=${VALUE//\"#ID\"/$RANDOM_ID}

echo "Producing task #${RANDOM_ID}"

docker-compose exec faust faust -A consumer send ORDERS "${VALUE}"
