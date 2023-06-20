#!/bin/bash

# Get the connected external display IDs dynamically
EXTERNAL_DISPLAYS=$(xrandr --query | grep ' connected' | grep -v 'eDP-1' | awk '{ print $1 }')

# Convert to an array
readarray -t EXTERNAL_DISPLAYS_ARRAY <<<"$EXTERNAL_DISPLAYS"

# Number of connected external displays
NUM_DISPLAYS=${#EXTERNAL_DISPLAYS_ARRAY[@]}

# Exit if no external displays are connected
if [ "$NUM_DISPLAYS" -eq 0 ]; then
    echo "No external displays are connected."
    exit 1
fi

# Get the status of the external displays
ACTIVE_DISPLAY=$(xrandr --query | grep ' connected' | grep '+0+0' | grep -v 'eDP-1' | awk '{ print $1 }')

# Toggle between the external displays
if [ "$ACTIVE_DISPLAY" == "${EXTERNAL_DISPLAYS_ARRAY[0]}" ]; then
    # If the first display is active, switch to the second display
    xrandr --output "${EXTERNAL_DISPLAYS_ARRAY[0]}" --off --output "${EXTERNAL_DISPLAYS_ARRAY[1]}" --auto
elif [ "$ACTIVE_DISPLAY" == "${EXTERNAL_DISPLAYS_ARRAY[1]}" ]; then
    # If the second display is active, switch to the first display
    xrandr --output "${EXTERNAL_DISPLAYS_ARRAY[1]}" --off --output "${EXTERNAL_DISPLAYS_ARRAY[0]}" --auto
else
    # If neither is active, turn on the first external display
    xrandr --output "${EXTERNAL_DISPLAYS_ARRAY[0]}" --auto
fi
