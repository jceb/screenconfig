# screenconfig

`screenconfig` is a tool automate the configuration of connected
screens/monitors.

## Usage

`screenconfig` is used as a command for the simple randr daemon
`srandrd`.  It shall be started through `srandrd` as follows:

    srandrd screenconfig

## Configuration

The configuration is stored in file
`~/.config/screenconfig/screenconfig.toml`.  My [personal
configuration](screenconfig.toml) should provide a good starting
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
    edids = ["E430044600000000"]
    # The path to a wallpaper can be specified for each screen.  The wallpaper is
    # set through the tool "feh"
    wallpaper = "~/wallpaper1920x1080.png"

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

    [monitors.benq.outputs.DP-1-1]

    [monitors.benq.outputs.HDMI1]
    # If you have multiple monitors with the same EDID that are connected at the
    # same time add the name of the output as the last element of the position to
    # set this monitor relative to it
    position = ["--left-of", "benq", "DP-1"]
    rotate = "left"
    wallpaper = "~/wallpaper2560x1440.png"

    [monitors.benq.outputs.DP-1-2]
    position = ["--left-of", "benq", "DP-1-1"]
    rotate = "left"
    wallpaper = "~/wallpaper2560x1440.png"

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

## Installation

* Install [`srandrd`](https://github.com/jceb/srandrd)
* Copy `screenconfig` to a directory in `$PATH`
* Create a personal configuration in
  `~/.config/screenconfig/screenconfig.toml`

## Related projects

- `srandrd` simple notification daemon of screen events
  [](https://github.com/jceb/srandrd)
