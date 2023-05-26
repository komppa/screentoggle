#!/bin/bash

# Get the display IDs dynamically
DISPLAYS=$(xrandr --query | grep ' connected' | awk '{ print $1 }')

# Get the status of the displays
DP1=$(echo $DISPLAYS | awk '{print $1}')
DP2=$(echo $DISPLAYS | awk '{print $2}')

DP1_STATUS=$(xrandr --query | grep "$DP1 connected")
DP2_STATUS=$(xrandr --query | grep "$DP2 connected")

# Check if DP1 is connected and active
if [[ $DP1_STATUS = *"+0+0"* ]]; then
    xrandr --output $DP2 --auto --output $DP1 --off
elif [[ $DP2_STATUS = *"+0+0"* ]]; then
    xrandr --output $DP1 --auto --output $DP2 --off
else
    # If neither is active, turn on DP1
    xrandr --output $DP1 --auto
fi
