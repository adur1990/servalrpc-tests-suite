#! /bin/bash

sudo pkill -9 vcmd
sudo pkill -9 python
sudo core-cleanup

if [[ "$1" == "a" ]]; then
    sudo rm -rf /tmp/*_server.csv /tmp/*_client.csv /tmp/.auto-scenario.log /tmp/serval* /tmp/netmon-n* /tmp/n* /tmp/pf_* /tmp/mf_* /tmp/tmp* /tmp/rpc_* /tmp/seed
fi
