#!/bin/bash
HOST=nonos-1

cd $(dirname $0)

# Upload source
rsync -a src pyproject.toml *.service *.sh $HOST:nonos_server;

# Load audio filter chain
ssh $HOST 'systemctl --user restart filter-chain.service'

sleep 1
ssh $HOST nonos_server/src/audio_server/processing/set_default.sh

# Get graph of pipewire
sleep 1
ssh $HOST 'pw-dot -o graph.dot' && rsync $HOST:graph.dot .
