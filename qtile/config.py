# ~/.config/qtile/config.py: executed when X11 starts.
# See https://docs.qtile.org/en/latest/manual/config/default.html
# for the default version Qtile writes automatically.
# ---
# Qtile - https://qtile.org/




import os
import subprocess
from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen, KeyChord
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
    Key([mod], "space", lazy.spawn("ulauncher-toggle"), desc="Launch ulauncher"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "Tab", lazy.screen.toggle_group(), desc="Last active group"),
    # ---
    KeyChord([mod], "q", [
            Key([], "1", lazy.group.setlayout("columns"), desc="Set columns layout"),
            Key([], "2", lazy.group.setlayout("floating"), desc="Set floating layout"),
            Key([], "3", lazy.group.setlayout("max"), desc="Set max layout")
        ],
        name="layoutmode"
    ),
    KeyChord([mod], "w", [
            Key([], "1", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
            Key([], "2", lazy.window.toggle_maximize(), desc="Toggle maximize on the focused window"),
            Key([], "3", lazy.window.toggle_minimize(), desc="Toggle minimize on the focused window"),
        ],
        name="winmode"
    ),
    Key([mod], "i", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "o", lazy.layout.toggle_split(), desc="Toggle between split and unsplit sides of stack"),
    Key([mod], "n", lazy.screen.next_group(), desc="Move focus to next group"),
    Key([mod], "p", lazy.screen.prev_group(), desc="Move focus to previews group"),
    Key([mod], "a", lazy.next_screen(), desc="Move focus to next monitor"),
    Key([mod], "s", lazy.layout.next(), desc="Move window focus to other window"),
    Key([mod], "d", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen on the focused window"),
    Key([mod], "g", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod], "z", lazy.spawn("diodon"), desc="Launch Diodon"),
    Key([mod], "x", lazy.spawn("firefox"), desc="Launch Firefox"),
    Key([mod], "c", lazy.spawn("code"), desc="Launch VSCode"),
    Key([mod], "v", lazy.spawn("gvim"), desc="Launch GVim"),
    Key([mod], "b", lazy.spawn("pcmanfm"), desc="Launch PCManFM"),
    Key([mod], "m", lazy.spawn(terminal), desc="Launch terminal"),
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
            Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True), desc="Switch to & move focused window to group {}".format(i.name))
        ]
    )


layouts = [
    layout.Columns(name="columns", border_on_single=True, border_width=3, margin=5),
    layout.Floating(name="floating", border_width=3),
    layout.Max(name="max", only_focused=False, border_width=3, margin=5),
]


widget_defaults = dict(font="Fira Code SemiBold", fontsize=13, padding=5)
extension_defaults = widget_defaults.copy()


screens = [
    Screen(
        wallpaper="~/.config/qtile/wallpaper",
        wallpaper_mode="fill",
        top=bar.Bar(
            [
                widget.CurrentLayoutIcon(scale=0.7),
                widget.GroupBox(highlight_method="line", highlight_color="#202020", rounded=False, disable_drag=True),
                widget.Sep(linewidth=2, padding=0, foreground="#000000"),
                widget.TaskList(max_title_width=200, icon_size=0, margin=0, padding_x=10, padding_y=4, rounded=False, spacing=5, highlight_method="block", unfocused_border="#202020",
                    mouse_callbacks={"Button1": lazy.window.toggle_maximize(), "Button3": lazy.window.toggle_minimize(), "Button2": lazy.window.kill()}
                ),
                widget.Sep(linewidth=5, padding=0, foreground="#000000"),
                widget.Chord(chords_colors={"winmode": ("#000000", "#00ffff"), "layoutmode": ("#000000", "#00ffff")}, name_transform=lambda name: name.upper()),
                widget.Prompt(prompt="RUN: ", padding=5, foreground="#00ffff", cursor_color="#ffffff"),
                widget.Systray(),
                widget.Sep(linewidth=5, padding=0, foreground="#000000"),
                widget.Volume(fmt="Vol {}", padding=10, background="#404040"),
                widget.Sep(linewidth=5, padding=0, foreground="#000000"),
                widget.Battery(format="Bat {char}{percent:2.0%}", padding=10, background="#404040"),
                widget.Sep(linewidth=5, padding=0, foreground="#000000"),
                widget.Clock(format="%a %d %b", padding=10, foreground="#ffff00", background="#404040"),
                widget.Sep(linewidth=5, padding=0, foreground="#000000"),
                widget.Clock(format="%I:%M %p", padding=10, background="#404040")
            ],
            24, border_width=[5, 0, 5, 0]
        )
    ),
    Screen(
        wallpaper="~/.config/qtile/wallpaper",
        wallpaper_mode="fill",
        top=bar.Bar(
            [
                widget.CurrentLayoutIcon(scale=0.7),
                widget.Sep(linewidth=2, padding=0, foreground="#000000"),
                widget.TaskList(max_title_width=200, icon_size=0, margin=0, padding_x=10, padding_y=4, rounded=False, spacing=5, highlight_method="block", unfocused_border="#202020",
                    mouse_callbacks={"Button1": lazy.window.toggle_maximize(), "Button3": lazy.window.toggle_minimize(), "Button2": lazy.window.kill()}
                ),
                widget.Sep(linewidth=5, padding=0, foreground="#000000"),
                widget.Chord(chords_colors={"winmode": ("#000000", "#00ffff"), "layoutmode": ("#000000", "#00ffff")}, name_transform=lambda name: name.upper()),
                widget.Sep(linewidth=5, padding=0, foreground="#000000"),
                widget.AGroupBox(fmt="Group {}", borderwidth=0, padding=0, margin_x=10, margin_y=3, background="#404040")
            ],
            24, border_width=[5, 0, 5, 0]
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
cursor_warp = True
floating_layout = layout.Floating(
    border_width=3,
    float_rules = [
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
