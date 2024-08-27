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

XRANDRID1="HDMI-1"
XRANDRID2="eDP-1"
WIDTHxHEIGHT="1024x768"
POSITION="--right-of"
ROTATION="half"
TOUCHPADID=$(xinput --list --name-only | grep -Eo '.*'"[Tt]ouch[Pp]ad"'.*' | head -n 1)
WACOMID=$(xsetwacom --list devices | grep -Eo '.*'"[Ww][Aa][Cc][Oo][Mm]"'.*' | head -n 1)
# ---
command xinput disable "$TOUCHPADID"
command xrandr --output "$XRANDRID2" --mode "$WIDTHxHEIGHT" "$POSITION" "$XRANDRID1"
command xsetwacom set "$WACOMID" MapToOutput "$XRANDRID2" rotate "$ROTATION"
