# screenconfig

`screenconfig` is a to automate the configuration of connected screens/monitors.

## Usage

`screenconfig` is used as a command for the simple randr daemon `srandrd`.  It
shall be started through `srandrd` as follows:

    srandrd screenconfig

## Configuration

The configuration is stored in file `~/.config/screenconfig/screenconfig.yaml`.
My [personal configuration](screenconfig.yaml) should provide a good starting
point:

    # this file format is described at https://en.wikipedia.org/wiki/YAML
    ---
    # The name of the top-level keys you can choose to your liking.
    # It's a good idea to give each of them an anchor (e.g. &laptop) so that it can
    # be referenced in other sections of the configuration
    laptop: &laptop
      # EDID is an identifier that is unique to each screen.  If you call `srandrd
      # list` it will provide an overview of the connected screens with their EDIDs
      edid: E430044600000000
      # The path to a wallpaper can be specified for each screen.  The wallpaper is
      # set through the tool "feh"
      wallpaper: ~/wallpaper1920x1080.png
    iiyama: &iiyama
      edid: CD2646B40000306A
      wallpaper: ~/wallpaper1280x1024.png
      # The position of this screen relative to another screen, in this case
      # relative to the screen with the "&laptop" anchor.  Position is one of
      # right-of, left-of, above, below or same-as
      position: {crtc: *laptop, position: right-of}
    samsung: &samsung
      edid: 2D4C03E800000000
      wallpaper: ~/wallpaper1920x1200.png
      position: {crtc: *laptop, position: left-of}
    dell: &dell
      edid: AC1040613239334C
      wallpaper: ~/wallpaper1920x1080.png

    # The default configuration that's applied if no other configuration matches.  A
    # different section can be selected by setting the environment variable
    # SCREENCONFIG_DEFAULT to the name of a different section.  This might be
    # useful to use the same configuration file for multiple computers.  Put the
    # following in your bashrc or window manager's start configuration
    # export SCREENCONFIG_DEFAULT="default-work"
    default:
      wallpaper: ~/wallpaper1920x1200.png
      # Resolution of this screen, either "auto" or a concrete resolution like
      # "800x600"
      resolution: auto
      position: {crtc: *laptop, position: above}

## Installation

* Install [`srandrd`](https://github.com/jceb/srandrd)
* Copy `screenconfig` to a directory in `$PATH`
* Create a personal configuration in `~/.config/screenconfig/screenconfig.yaml`

## Related projects

- `srandrd` simple notification daemon of screen events https://github.com/jceb/srandrd
