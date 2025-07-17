#!/bin/bash
HOST=nonos-1

cd $(dirname $0)

# Upload source
rsync -a src pyproject.toml services *.sh $HOST:nonos_server;

# Load audio filter chain
ssh $HOST 'nonos_server/.venv_pi/bin/python nonos_server/src/audio_server/processing/chain.py'


# Get graph of pipewire
sleep 1
ssh $HOST 'pw-dot -o graph.dot' && rsync $HOST:graph.dot .
