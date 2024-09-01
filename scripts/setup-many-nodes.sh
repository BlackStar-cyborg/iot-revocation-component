#!/usr/bin/env bash
set -e

NUMBER_NODES=$1
INCREMENT=10
START_PORT=8100
END_PORT=$((START_PORT + NUMBER_NODES * INCREMENT))
NAME_PREFIX="controller_node_"
PAUSE_DURATION=60 # Duration to pause between batches in seconds, to prevent overwhelming docker
BATCH_SIZE=5

mkdir -p logs .agent_cache
for ((i = START_PORT; i < END_PORT; i += INCREMENT * BATCH_SIZE)); do
  for ((j = i; j < i + INCREMENT * BATCH_SIZE && j < END_PORT; j += INCREMENT)); do
    (
      echo "Running node: $j"
      echo "Node name: $NAME_PREFIX$j"
      ./run --background --type node --port $j --name "$NAME_PREFIX$j" &>./logs/"$NAME_PREFIX$j" || echo "Error starting node $NAME_PREFIX$j" >> error.log
      echo "Initialization started $NAME_PREFIX$j"
    ) &
  done
  echo "Pausing for $PAUSE_DURATION seconds..."
  sleep $PAUSE_DURATION
done