#! /bin/bash

# Global defines. Make changes easier.
WATCH_AGENT_TIME=2400
NUM_CALLS=10


# Clean the directory before doing anything.
mkdir -p autorun_confs
rm -f autorun_confs/full.conf
rm -f autorun_confs/hub.conf
rm -f autorun_confs/chain.conf
rm -f autorun_confs/islands.conf

# First special case: idle
echo "core idle \"\" \"\" \"\" -a #3 hub" | tee -a autorun_confs/hub.conf >> autorun_confs/full.conf
echo "core idle \"\" \"\" \"\" -a #3 chain" | tee -a autorun_confs/chain.conf >> autorun_confs/full.conf

for d in */*; do
    # Skip this folders.
    if [[ $d == *"evaluation"* ]]; then
        continue
    fi

    if [[ $d == *"autorun"* ]]; then
        continue
    fi

    if [[ $d == *"evaluation"* ]]; then
        continue
    fi

    if [[ $d == *"idle"* ]]; then
        continue
    fi

    if [[ $d == *"combined"* ]]; then
        continue
    fi

    if [[ $d == *"topologies"* ]]; then
        continue
    fi

    if [[ $d == *"noise"* ]]; then
        continue
    fi

    # If all special files are skipped, just echo the tests to the right file.
    echo "core $d \"\" \"$WATCH_AGENT_TIME\" \"$NUM_CALLS\" 0 #3 hub" | tee -a autorun_confs/hub.conf >> autorun_confs/full.conf
    echo "core $d \"\" \"$WATCH_AGENT_TIME\" \"$NUM_CALLS\" 0 #3 chain" | tee -a autorun_confs/chain.conf >> autorun_confs/full.conf
    echo "core $d \"\" \"$WATCH_AGENT_TIME\" \"$NUM_CALLS\" 0 #3 islands" | tee -a autorun_confs/islands.conf >> autorun_confs/full.conf
    
    echo "core $d \"\" \"$WATCH_AGENT_TIME\" \"$NUM_CALLS\" -a #3 hub" | tee -a autorun_confs/hub.conf >> autorun_confs/full.conf
    echo "core $d \"\" \"$WATCH_AGENT_TIME\" \"$NUM_CALLS\" -a #3 chain" | tee -a autorun_confs/chain.conf >> autorun_confs/full.conf
    echo "core $d \"\" \"$WATCH_AGENT_TIME\" \"$NUM_CALLS\" -a #3 islands" | tee -a autorun_confs/islands.conf >> autorun_confs/full.conf
done

# Second special case: combined
echo "core combined \"\" \"$WATCH_AGENT_TIME\" \"$NUM_CALLS\" 0 #3 hub" | tee -a autorun_confs/hub.conf >> autorun_confs/full.conf
echo "core combined \"\" \"$WATCH_AGENT_TIME\" \"$NUM_CALLS\" 0 #3 chain" | tee -a autorun_confs/chain.conf >> autorun_confs/full.conf
echo "core combined \"\" \"$WATCH_AGENT_TIME\" \"$NUM_CALLS\" 0 #3 islands" | tee -a autorun_confs/islands.conf >> autorun_confs/full.conf

echo "core combined \"\" \"$WATCH_AGENT_TIME\" \"$NUM_CALLS\" -a #3 hub" | tee -a autorun_confs/hub.conf >> autorun_confs/full.conf
echo "core combined \"\" \"$WATCH_AGENT_TIME\" \"$NUM_CALLS\" -a #3 chain" | tee -a autorun_confs/chain.conf >> autorun_confs/full.conf
echo "core combined \"\" \"$WATCH_AGENT_TIME\" \"$NUM_CALLS\" -a #3 islands" | tee -a autorun_confs/islands.conf >> autorun_confs/full.conf
