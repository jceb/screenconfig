# screenconfig

`screenconfig` is a tool automate the configuration of connected
monitors.

Why is that useful?  Suppose you have a laptop that you use at work, at
home, and on the road and you frequently connect it to various
monitors.  The monitors might be in different positions relative to your
laptop.  This will cause you to repeatedly run `xrandr` and potentially
other commands for setting your wallpaper also.
`screenconfig` set out to fix this by providing a simple file format
that stores your preferences and an automated integration with `xrandr`
that will do the hard work of executing the necessary commands to
adapt the monitors to your preferences.

## Installation

* Install [`feh`](https://feh.finalrewind.org/)
* Install [`srandrd`](https://github.com/jceb/srandrd)
* Install [`screenconfig`](https://github.com/jceb/screenconfig), e.g.
  run `./setup.py install --user`
* Create a personal configuration in
  `~/.config/screenconfig/screenconfig.toml`.  Here is an
  [example](screenconfig/screenconfig.toml).

## Usage

`screenconfig` is used as a command for the simple randr daemon
[`srandrd`](https://github.com/jceb/srandrd).  It shall be started
through `srandrd` as follows:

    srandrd -e screenconfig

For testing purposes it's helpful to run `srandrd` in foreground and in
verbose mode:

    srandrd -v -n -e screenconfig

## Configuration

The configuration is stored in file
`~/.config/screenconfig/screenconfig.toml`.  My [personal
configuration](screenconfig/screenconfig.toml) should provide a good starting
point:

    title = "Screen configuration"

    [monitors]

    # The name of the top-level keys you can choose to your liking but they have to
    # start with "monitors".
    [monitors.laptop]
    description = "Laptop"
    # EDID is an identifier that is unique to each screen.  If you call
    # `srandrd list` it will provide an overview of the connected screens with their
    # EDIDs
    edids = ["E430044600000000", "7038000000000000"]
    # The path to a wallpaper can be specified for each screen.  The wallpaper is
    # set through the tool "feh"
    wallpaper = "~/wallpaper1920x1080.png"
    # List of commands that are executed when a monitor is connected or disconnected
    # - All SRANDRD_* environment variables of the event are available to the
    #   command and can be used by it.  If the command is prefixed with
    #   ["sh", "-c", ...] the variables can be used directly in the command's
    #   arguments.
    # - The event parameters can also be used in the command's arguments with the
    #   python string formatting syntax: {.ATTRIBUTE}.  The following attributes are
    #   available:
    #   - event: either connected or disconnected
    #   - output: name of the xrandr output that triggered the event
    #   - edid: EDID of the monitor
    #   - screenid: XINERAMA screen id
    # exec_on_connect = [
    # ["touch", "/tmp/test/file"],
    # ["sh", "-x", "-c", "touch /tmp/test/$SRANDRD_EVENT"],
    # ["touch", "/tmp/test/{.output}"]
    # ]
    # Don't specify exec_on_disconnect here, it will never be triggered
    # because EDID is not available!
    # exec_on_disconnect = [
    # ]

    [monitors.iiyama]
    description = "Iiyama"
    edids = ["CD2646B40000306A"]
    wallpaper = "~/wallpaper1280x1024.png"
    # The position of this screen relative to another screen, in this case
    # relative to the screen "laptop".  Position is one of
    # --right-of, --left-of, --above, --below or --same-as
    # (see xrandr(1) for more information)
    position = ["--left-of", "laptop"]

    [monitors.benq]
    description = "Benq BL1152"
    edids = ["D109801B00005445"]
    position = ["--left-of", "laptop"]
    wallpaper = "~/wallpaper2560x1440.png"

    # It is possible to provide specific configuration details depending on the
    # output that the monitor is connected to.  The string ".outputs." followed
    # name of the output (run xrandr to get the name) is appended to the monitor
    # configuration section.  All configurations options can be used in this
    # subsection
    [monitors.benq.outputs.DP-1]

    [monitors.benq.outputs.DP1-1]

    [monitors.benq.outputs.DP-1-1]

    [monitors.benq.outputs.HDMI1]

    [monitors.benq.outputs.HDMI2]
    # If you have multiple monitors with the same EDID that are connected at the
    # same time add the name of the output as the last element of the position to
    # set this monitor relative to it
    position = ["--left-of", "benq", "HDMI1"]
    xrandr_args = ["--rotate", "left"]
    wallpaper = "~/wallpaper1440x2560.png"

    [monitors.benq.outputs.DP1-2]
    position = ["--left-of", "benq", "DP1-1"]
    xrandr_args = ["--rotate", "left"]
    wallpaper = "~/wallpaper1440x2560.png"

    [monitors.benq.outputs.DP-1-2]
    position = ["--left-of", "benq", "DP-1-1"]
    xrandr_args = ["--rotate", "left"]
    wallpaper = "~/wallpaper1440x2560.png"

    [monitors.samsung]
    description = "Samsung"
    edids = ["2D4C03E800000000", "2D4C03E654573236"]
    position = ["--left-of", "laptop"]
    wallpaper = "~/wallpaper1920x1200.png"

    [monitors.dell]
    description = "Dell"
    edids = ["AC1040613239334C"]
    wallpaper = "~/wallpaper1920x1080.png"

    [monitors.univentionbeamer]
    description = "Acer"
    edids = ["7204870100001893"]
    # Resolution of this screen, either "auto" or a concrete resolution like
    # "800x600"
    resolution = "1280x1024"
    wallpaper = "~/wallpaper1280x1024.png"

    # The default configuration that's applied if no other configuration matches.  A
    # different section can be selected by setting the environment variable
    # SCREENCONFIG_DEFAULT to the name of a different section.  This might be
    # useful to use the same configuration file for multiple computers.
    #
    # E.g. put the following in your work computer's bashrc
    # export SCREENCONFIG_DEFAULT="monitors.default-work"
    [monitors.default]
    position = ["--right-of", "laptop"]
    resolution = "auto"
    wallpaper = "~/wallpaper1920x1200.png"
    # exec_on_connect = [
    # ["touch", "/tmp/test/file"],
    # ["sh", "-x", "-c", "touch /tmp/test/$SRANDRD_EVENT"],
    # ["touch", "/tmp/test/{.output}"]
    # ]
    # The disconnect commands will only be triggered from the default
    # configuration because EDID is not available!
    # exec_on_disconnect = [
    # ]

## Related projects

- [`autorandr`](https://github.com/phillipberndt/autorandr) Auto-detect the connected display hardware and load the appropriate X11 setup using xrandr
- [`srandrd`](https://github.com/jceb/srandrd) simple notification daemon of screen events
