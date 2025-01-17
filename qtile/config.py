# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
from Vertical_Stack import VStack
from libqtile import bar, layout, qtile, widget
from libqtile.config import (
    Click,
    Drag,
    Group,
    Key,
    Match,
    Screen,
    ScratchPad,
    DropDown,
    KeyChord,
)
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

mod = "mod4"
terminal = guess_terminal()

keys = [
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    # Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    Key(
        [mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"
    ),
    Key(
        [mod, "shift"],
        "l",
        lazy.layout.shuffle_right(),
        desc="Move window to the right",
    ),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key(
        [mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"
    ),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Space", lazy.next_screen(), desc="Focus Next Monitor"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.spawn("rofi -show window"), desc="Toggle between layouts"),
    Key([mod, "control"], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key(
        [mod],
        "t",
        lazy.window.toggle_floating(),
        desc="Toggle floating on the focused window",
    ),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key(
        [mod],
        "r",
        lazy.spawn("rofi -show drun"),
        desc="Spawn a command using a prompt widget",
    ),
    Key([mod, "shift"], "s", lazy.spawn("flameshot gui"), desc="Take a screenshot"),
    Key([mod], "q", lazy.spawn("chromium"), desc="Launch Brave Browser"),
    Key(
        [mod, "control"],
        "space",
        lazy.widget["keyboardlayout"].next_keyboard(),
        desc="toggle keyboardLayout",
    ),
    Key([mod, "control"], "1", lazy.to_screen(0)),
    Key([mod, "control"], "2", lazy.to_screen(2)),
    Key([mod, "control"], "3", lazy.to_screen(1)),
    Key([mod], "F3", lazy.spawn("/home/egilmore/Projects/dm-scripts/scrpy.sh")),
    KeyChord(
        [mod],
        "space",
        [
            Key(
                [],
                "1",
                lazy.spawn(
                    "/home/egilmore/Projects/dm-scripts/networkmanager-dmenu/networkmanager_dmenu"
                ),
            ),
            Key(
                [],
                "s",
                lazy.spawn("/home/egilmore/Projects/dm-scripts/adb_push_screenshot.sh"),
            ),
            Key(
                [], "c", lazy.spawn("/home/egilmore/Projects/dm-scripts/edit-config.sh")
            ),
            Key(
                [],
                "0",
                lazy.spawn("/home/egilmore/Projects/dm-scripts/screen-layout.sh"),
            ),
            Key(
                [],
                "3",
                lazy.spawn("/home/egilmore/Projects/dm-scripts/scrcpy_selector.sh"),
            ),
            Key([], "4", lazy.spawn("/home/egilmore/Projects/dm-scripts/pulse.sh")),
            Key([], "2", lazy.spawn("/home/egilmore/Projects/dm-scripts/remmina.sh")),
        ],
        mode=False,
        name="dmenu",
    ),
    #        KeyChord([mod], "z", [
    #            Key([], 'F1', lazy.group['scratch'].dropdown_toggle('term')),
    #            Key([], 'F2', lazy.group['scratch'].dropdown_toggle('btop')),
    #            Key([], 'F3', lazy.group['scratch'].dropdown_toggle('nnn')),
    #            Key([], 'F9', lazy.group['scratch'].dropdown_toggle('whatsapp')),
    #            Key([], 'F10', lazy.group['scratch'].dropdown_toggle('telegram')),
    #            Key([], 'F11', lazy.group['scratch'].dropdown_toggle('teams')),
    #            Key([], 'F12', lazy.group['scratch'].dropdown_toggle('mail'))],
    #        mode=False,
    #    name='REMOTE'
    #    )
]

for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )

groups = []
##### GROUP LIST #####
groups_list = []
group_names = ["1", "2", "3", "4", "5"]
group_labels = ["WWW", "DEV", "SYS", "DOC", "CHAT"]
group_layouts = ["max", "max", "max", "max", "max"]

for i in range(len(group_names)):
    groups_list.append(
        Group(
            name=group_names[i], layout=group_layouts[i].lower(), label=group_labels[i]
        )
    )

##### GROUPS KEYS ####
groups_keys = []
for i in groups_list:
    groups_keys.extend(
        [
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="",
            ),
            Key(
                [mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=False)
            ),
        ],
    )

##### SCRATCHS #####
scratchs = [
    ScratchPad(
        "scratch",
        [
            DropDown(
                "scrcpy",
                "scrcpy -s 4bc05ad2 --mouse=aoa --mouse-bind=++++:bhsn --no-video --no-audio --no-cleanup --power-off-on-close --keyboard=aoa",
                x=0.05,
                y=0.4,
                width=0.9,
                height=0.6,
                opacity=0.9,
            ),
            DropDown(
                "term",
                "alacritty -e tmux",
                x=0.05,
                y=0.4,
                width=0.9,
                height=0.6,
                opacity=0.9,
            ),
            DropDown(
                "nnn",
                "alacritty -e nnn",
                x=0.05,
                y=0.4,
                width=0.9,
                height=0.6,
                opacity=0.9,
            ),
            DropDown(
                "calculator",
                "gnome-calculator",
                x=0,
                y=0.4,
                width=0.09,
                height=0.6,
                opacity=1,
            ),
            DropDown("obs", "obs", x=0.05, y=0.4, width=0.9, height=0.6, opacity=1),
        ],
    )
]

##### SCRATCHS KEYS #####
scratchs_keys = [
    Key([mod], "F1", lazy.group["scratch"].dropdown_toggle("term")),
    Key([mod], "F2", lazy.group["scratch"].dropdown_toggle("nnn")),
    # F3 IS SCRCPY DEFINED IN THE KEYS ADOVE
    Key([mod], "F4", lazy.group["scratch"].dropdown_toggle("calculator")),
    Key([mod], "g", lazy.group["scratch"].dropdown_toggle("obs")),
]

##### GROUPS ####
groups.extend(groups_list)
groups.extend(scratchs)

##### GROUPS KEYS #####
keys.extend(groups_keys)
keys.extend(scratchs_keys)


layouts = [
    layout.MonadTall(),
    layout.Max(),
    layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4),
    layout.Stack(num_stacks=2),
    # VStack(num_stacks=2),
    layout.VerticalTile(
        border_focus="#0000ff",  # Focused window border color
        border_normal="#000000",  # Unfocused window border color
        border_width=1,  # Border width
        margin=0,  # Margin around the layout
        num_stacks=2,  # Number of stacks
    ),
    # Try more layouts by unleashing below layouts.
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="JetBrains Mono",
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.CurrentLayoutIcon(scale=0.8),
                widget.GroupBox(),
                widget.Prompt(),
                widget.WindowName(),
                widget.Chord(
                    chords_colors={
                        "launch": ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                # NB Systray is incompatible with Wayland, consider using StatusNotifier instead
                # widget.StatusNotifier(),
                widget.Systray(),
                widget.KeyboardLayout(
                    configured_keyboards=["latam", "us"],
                    display_map={"latam": "la", "us": "us"},
                ),
                widget.Clock(format="%Y-%m-%d %a %I:%M %p"),
                widget.Battery(),
                widget.WindowCount(),
                widget.CurrentScreen(),
                # widget.QuickExit(),
            ],
            24,
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
        # You can uncomment this variable if you see that on X11 floating resize/moving is laggy
        # By default we handle these events delayed to already improve performance, however your system might still be struggling
        # This variable is set to None (no cap) by default, but you can set it to 60 to indicate that you limit it to 60 events per second
        # x11_drag_polling_rate = 60,
    ),
    Screen(
        top=bar.Bar(
            [
                widget.CurrentLayoutIcon(scale=0.8),
                widget.GroupBox(),
                widget.Prompt(),
                widget.WindowName(),
                widget.Chord(
                    chords_colors={
                        "launch": ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                # NB Systray is incompatible with Wayland, consider using StatusNotifier instead
                # widget.StatusNotifier(),
                widget.KeyboardLayout(
                    configured_keyboards=["latam", "us"],
                    display_map={"latam": "la", "us": "us"},
                ),
                widget.Clock(format="%Y-%m-%d %a %I:%M %p"),
                widget.Battery(),
                widget.WindowCount(),
                widget.CurrentScreen(),
                # widget.QuickExit(),
            ],
            24,
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
        # You can uncomment this variable if you see that on X11 floating resize/moving is laggy
        # By default we handle these events delayed to already improve performance, however your system might still be struggling
        # This variable is set to None (no cap) by default, but you can set it to 60 to indicate that you limit it to 60 events per second
        # x11_drag_polling_rate = 60,
    ),
    Screen(
        top=bar.Bar(
            [
                widget.CurrentLayoutIcon(scale=0.8),
                widget.GroupBox(),
                widget.Prompt(),
                widget.WindowName(),
                widget.Chord(
                    chords_colors={
                        "launch": ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                # NB Systray is incompatible with Wayland, consider using StatusNotifier instead
                # widget.StatusNotifier(),
                widget.KeyboardLayout(
                    configured_keyboards=["latam", "us"],
                    display_map={"latam": "la", "us": "us"},
                ),
                widget.Clock(format="%Y-%m-%d %a %I:%M %p"),
                widget.Battery(),
                widget.WindowCount(),
                widget.CurrentScreen(),
                # widget.QuickExit(),
            ],
            24,
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
        # You can uncomment this variable if you see that on X11 floating resize/moving is laggy
        # By default we handle these events delayed to already improve performance, however your system might still be struggling
        # This variable is set to None (no cap) by default, but you can set it to 60 to indicate that you limit it to 60 events per second
        # x11_drag_polling_rate = 60,
    ),
]

# Drag floating layouts.
mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = True
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# xcursor theme (string or None) and size (integer) for Wayland backend
wl_xcursor_theme = None
wl_xcursor_size = 24

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
