#!/bin/bash

filters=($(cat $(dirname $0)/chain.conf | grep 'plugin\s*=' | sed -r 's/.*plugin\s*=\s*"([^"]+)".*/\1/' | sort | uniq))

for f in "${filters[@]}"; do
    if [ ! -f "$f" ]; then
        echo "Filter $f not found"
        continue
    fi
    analyseplugin $f
done
