#!/bin/bash

SSH="ssh -o StrictHostKeyChecking=no"
SCRIPT="private/route_planner/run.sh"
#SCRIPT="killall python"

for i in $(seq 20 40); do
    ${SSH} hpm14@ray${i} ${SCRIPT}&
    sleep 5s
done
