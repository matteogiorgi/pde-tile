#!/bin/sh

# ~/.xinitrc: executed after logging in by xinit (invoked via startx).
# First you log in on a text console, then you start the GUI with startx.
# ---
# https://wiki.debian.org/Xinitrc




exec qtile 2>~/.qtile.err
