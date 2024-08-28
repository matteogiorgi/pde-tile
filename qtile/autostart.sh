#!/usr/bin/env bash

# ~/.config/qtile/autostart.sh: execute the
# programs you want to run when qtile starts.
# Ulauncher is not included in Debian repos,
# intall it separately from https://ulauncher.io/.
# ---
# See https://docs.qtile.org/en/latest/manual/config/hooks.html#autostart
# for all the details on how to run programs when qtile starts.




### Defaults
############

command lxpolkit &
command nm-applet &
command diodon &
command flameshot &
command pcmanfm -d &
command nitrogen --restore &
command ulauncher --hide-window --no-window-shadow &
command setxkbmap us -option "caps:swapescape"




### Custom
##########

SCREEN1_ID="eDP-1"
SCREEN2_ID="HDMI-1"
SCREEN2_POSITION="--right-of"
SCREEN2_RATIO="1024x768"
TOUCH_ID=$(xinput --list --name-only | grep -Eo '.*'"[Tt]ouch[Pp]ad"'.*' | head -n 1)
WACOM_ID=$(xinput --list --name-only | grep -Eo '.*'"[Ww][Aa][Cc][Oo][Mm].*[Ss]tylus"'.*' | head -n 1)
WACOM_ROTATION="half"
# ---
command xinput disable "$TOUCH_ID"
command xsetwacom set "$WACOM_ID" rotate "$WACOM_ROTATION"
if xrandr | grep "$SCREEN1_ID" | grep "$SCREEN2_ID"; then
    command xrandr --output "$SCREEN2_ID" --mode "$SCREEN2_RATIO" "$SCREEN2_POSITION" "$SCREEN1_ID"
    command xsetwacom set "$WACOM_ID" MapToOutput "$SCREEN2_ID" rotate "$WACOM_ROTATION"
fi
