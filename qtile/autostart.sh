#!/usr/bin/env bash

# ~/.config/qtile/autostart.sh: execute the
# programs you want to run when qtile starts.
# Ulauncher is not included in Debian repos,
# intall it separately from https://ulauncher.io/.
# ---
# See https://docs.qtile.org/en/latest/manual/config/hooks.html#autostart
# for all the details on how to run programs when qtile starts.




command nm-applet &
command diodon &
command flameshot &
command ulauncher --hide-window --no-window-shadow &
command setxkbmap us -option "caps:swapescape"
