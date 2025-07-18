#!/bin/bash

chaininput=$(pw-dump | jq '.[] | select(.type == "PipeWire:Interface:Node" and .info.props["node.name"] == "Speaker-Master-Input") | .id')

if [ -z "$chaininput" ]; then
    echo "Node not found"
    exit 1
fi

echo "Setting default to $chaininput"
wpctl set-default $chaininput

chainoutname=Speaker-Master-Output
outname=alsa_output.platform-soc_107c000000_sound.stereo-fallback

# accept already linked ports
pw-link $chainoutname:capture_FL $outname:playback_FL
rc=$?
if [ $rc -ne 0 ] && [ $rc -ne 255 ]; then
    echo "Error linking ports"
    exit 2
fi

pw-link $chainoutname:capture_FR $outname:playback_FR
rc=$?
if [ $rc -ne 0 ] && [ $rc -ne 255 ]; then
    echo "Error linking ports"
    exit 2
fi