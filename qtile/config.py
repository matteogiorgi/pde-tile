# ~/.config/qtile/config.py: executed when X11 starts.
# See https://docs.qtile.org/en/latest/manual/config/default.html
# for the default version.
# ---
# Qtile - https://qtile.org/




import os
import subprocess
from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile import hook


@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser("~/.config/qtile/autostart.sh")
    subprocess.Popen([home])


@lazy.window.function
def window_to_group(window, direction="next"):
    index = window.qtile.groups.index(window.group)
    if direction == "next":
        index = (index + 1) % len(window.qtile.groups)
    elif direction == "prev":
        index = (index - 1) % len(window.qtile.groups)
    target_group = window.qtile.groups[index]
    window.cmd_togroup(target_group.name)
    window.qtile.current_screen.set_group(target_group)


mod = "mod4"
terminal = guess_terminal()


keys = [
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    # ---
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # ---
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    # ---
    Key([mod], "space", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "s", lazy.layout.toggle_split(), desc="Toggle between split and unsplit sides of stack"),
    Key([mod], "w", lazy.layout.next(), desc="Move window focus to other window"),
    # ---
    Key([mod], "i", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod], "o", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen on the focused window"),
    Key([mod], "n", lazy.screen.next_group(), desc="Move focus to next group"),
    Key([mod], "p", lazy.screen.prev_group(), desc="Move focus to previews group"),
    # ---
    Key([mod, "shift"], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "shift"], "n", window_to_group("next"), desc="Move window to next group"),
    Key([mod, "shift"], "p", window_to_group("prev"), desc="Move window to previews group"),
    # ---
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod, "control"], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # ---
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer set Master 5%- unmute"), desc="Low volume"),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer set Master 5%+ unmute"), desc="Raise volume"),
    Key([], "XF86AudioMute", lazy.spawn("amixer -D pulse set Master 1+ toggle"), desc="Mute volume"),
    Key([], "XF86AudioMicMute", lazy.spawn("amixer set Capture togglemute"), desc="Mute mic"),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 10%-"), desc="Low brightness"),
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set +10%"), desc="Raise brightness")
]


groups = [Group(i) for i in "1234567890"]
for i in groups:
    keys.extend(
        [
            Key([mod], i.name, lazy.group[i.name].toscreen(), desc="Switch to group {}".format(i.name)),
            Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name)
            )
        ]
    )


layouts = [
    layout.Columns(border_width=3),
    layout.Max()
]


widget_defaults = dict(font="Fira Code Bold", fontsize=13, padding=5)
extension_defaults = widget_defaults.copy()


screens = [
    Screen(
        wallpaper="~/.config/qtile/wallpaper.png",
        wallpaper_mode="fill",
        top=bar.Bar(
            [
                widget.CurrentLayoutIcon(scale=0.7),
                widget.GroupBox(highlight_method="line", highlight_color="#202020", disable_drag="True"),
                widget.Prompt(prompt="> ", foreground="#000000", background="#ffe300", cursor_color="#ff0000"),
                widget.WindowName(),
                widget.Chord(chords_colors={"launch": ("#ff0000", "#ffffff")}, name_transform=lambda name: name.upper()),
                widget.Systray(),
                widget.Sep(linewidth=5, padding=0, foreground="#000000"),
                widget.Volume(fmt="vol {}", padding=10, background="#404040"),
                widget.Sep(linewidth=5, padding=0, foreground="#000000"),
                widget.Battery(format="bat {percent:2.0%}", padding=10, background="#404040"),
                widget.Sep(linewidth=5, padding=0, foreground="#000000"),
                widget.Clock(format="%a %d %b", padding=10, foreground="#ffe300", background="#404040"),
                widget.Sep(linewidth=5, padding=0, foreground="#000000"),
                widget.Clock(format="%I:%M %p", padding=10, background="#404040"),
            ],
            24, border_width=[3, 0, 3, 0]
        )
    )
]


mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]


dgroups_key_binder = None
dgroups_app_rules = []
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    border_width=3,
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),
        Match(wm_class="makebranch"),
        Match(wm_class="maketag"),
        Match(wm_class="ssh-askpass"),
        Match(title="branchdialog"),
        Match(title="pinentry")
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True


auto_minimize = True
wl_input_rules = None
wmname = "LG3D"
