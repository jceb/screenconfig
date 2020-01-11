#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# See LICENSE for copyright and license details

import toml
import os
import sys
import subprocess
import functools

version = '2018.10'

CONNECTED = 'connected'
DISCONNECTED = 'disconnected'


CONFIG_FILE = os.path.expandvars(os.path.join(
        os.environ.get('XDG_CONFIG_HOME',
                       os.path.join('$HOME', '.config')),
        'screenconfig',
        'screenconfig.toml'))

DEFAULT_MONITOR = 'default'


class Event():
    def __init__(self, output=None, event=None, edid=None, screenid=None):
        self.event = event
        self.output = output
        self.edid = edid
        self.screenid = screenid


class MonitorConfiguration():
    def __init__(self, monitor_config):
        """
        @param :monitor_config: monitor configuration
        """
        self.monitor_config = monitor_config

    def __str__(self):
        return str(self.monitor_config)

    def __getattr__(self, name):
        if self.monitor_config:
            return self.monitor_config.get(name, None)

    def get(self, name, default=None):
        if name in self.monitor_config:
            return self.monitor_config[name]
        else:
            return default


class GlobalConfiguration():
    def __init__(self, outputs, monitors_config, default_monitor):
        """
        @param :outputs: dict of outputs and edids of the connected monitors
        @param :monitors_config: monitor configuration
        @param :default_monitor: default monitor in the configuration
        """
        self.outputs = outputs
        self.monitors_config = monitors_config
        self.default_monitor = default_monitor

    def __str__(self):
        return str(self.outputs, self.monitor_config, self.default_monitor)

    def __getattr__(self, name):
        if self.monitors:
            return self.monitors.get(name, None)

    @property
    def monitors(self):
        return self.monitors_config['monitors']

    @property
    def default(self):
        if self.monitors:
            return self.monitors[self.default_monitor]


def first(l):
    if l:
        for e in l:
            return e


def compose(*funcs):
    """Return a new function s.t.
       compose(f,g,...)(x) == f(g(...(x)))"""
    def inner(*args):
        result = args
        for f in reversed(funcs):
            if type(result) in (list, tuple):
                result = f(*result)
            else:
                result = f(result)
        return result
    return inner


def jam(*funcs):
    """Return a new function s.t.
       jam(f,g,...)(x) == g(x), f(x)"""
    def inner(*args):
        for f in reversed(funcs):
                f(*args)
    return inner


def _execute(f, cmd, *args, **kwargs):
    # print('_execute: ', ' '.join(cmd))
    return f(cmd, *args, **kwargs)


def execute(cmd, *args, **kwargs):
    return _execute(subprocess.call, cmd, *args, **kwargs)


def check_output(cmd, *args, **kwargs):
    return _execute(subprocess.check_output, cmd, *args, **kwargs)


def get_connected_outputs():
    """
    @returns dict {output: edid}
    """
    return {output_edid[0]: output_edid[1] if len(output_edid) == 2 else None
            for line in check_output(
                ['srandrd', 'list']).decode('utf-8').strip().split(os.linesep)
            for output_edid in (line.split(' ', 1), )
            }


def merge_monitor_config(default_config, monitor_config, output=None):
    merged_config = default_config.copy()
    if monitor_config:
        merged_config.update(monitor_config)

    if output:
        merged_config.update(
            monitor_config.get('outputs', {})
            .get(output, {}))

    if 'outputs' in merged_config:
        del merged_config['outputs']
    return merged_config


def get_monitor_configuration(config, monitor, output=None):
    assert config and monitor

    return MonitorConfiguration(
        merge_monitor_config(config.default,
                             first(map(
                                 config.monitors.get,
                                 filter(lambda m: m == monitor,
                                        config.monitors.keys())
                             )),
                             output))


def get_mon_configuration_for_edid(config, edid=None, output=None):
    if not config:
        return None

    # find the right configuration, might be multiple if the configuration
    # specifies the edid multiple times
    monitor_config = first(filter(None, [
        c if edid in c.get('edids', [])
        or edid in c.get('outputs', {}).get(output, {}).get('edids', [])
        else None
        for c in config.monitors.values()
    ]))

    if not monitor_config:
        return MonitorConfiguration(config.default)

    # use the first configuration merge configuration
    return MonitorConfiguration(
        merge_monitor_config(config.default,
                             monitor_config, output))


def get_wallpaper(monitor_config):
    if monitor_config and monitor_config.wallpaper:
        return os.path.expandvars(os.path.expanduser(monitor_config.wallpaper))


def set_wallpapers(config, event, commands):
    wallpapers = list(filter(None, map(
        lambda output, edid: compose(get_wallpaper,
                                     get_mon_configuration_for_edid)(config,
                                                                     edid,
                                                                     output),
        config.outputs.keys(),
        config.outputs.values()
    )))

    if wallpapers:
        commands.append(['feh', '--bg-fill', '--no-fehbg'] + wallpapers)
    return config, event, commands


def find_reference_output(config, reference_monitor, _reference_output=None):
    if _reference_output:
        return _reference_output

    reference_monitor_config = get_monitor_configuration(config,
                                                         reference_monitor,
                                                         _reference_output)
    reference_output = first(filter(None, map(
        lambda output, edid: output
        if edid in reference_monitor_config.edids else None,
        config.outputs.keys(),
        config.outputs.values()
    )))
    if reference_output:
        return reference_output


def format_cmd(event, cmd):
    return [arg.format(event) for arg in cmd]


def get_commands(event, cmdlist):
    if cmdlist:
        return [format_cmd(event, cmd) for cmd in cmdlist]
    return []


def activate_crtc(config, event, commands):
    monitor_config = get_mon_configuration_for_edid(config,
                                                    event.edid,
                                                    event.output)
    if not monitor_config:
        return None

    xrandr_cmd = ['xrandr', '--output', event.output]
    resolution = monitor_config.resolution
    if not resolution or resolution == 'auto':
        xrandr_cmd.append('--auto')
    else:
        xrandr_cmd.extend(('--mode', resolution))

    if monitor_config.xrandr_args:
        xrandr_cmd.extend(monitor_config.xrandr_args)

    if monitor_config.position and len(monitor_config.position) >= 2:
        reference_output = find_reference_output(config,
                                                 *monitor_config.position[1:3])
        if reference_output and reference_output != event.output:
            xrandr_cmd.extend((monitor_config.position[0], reference_output))

    commands.append(xrandr_cmd)
    commands.extend(get_commands(event, monitor_config.exec_on_disconnect))
    return config, event, commands


def deactivate_crtc(config, event, commands):
    monitor_config = get_mon_configuration_for_edid(config,
                                                    event.edid,
                                                    event.output)

    commands.append(['xrandr', '--output', event.output, '--off'])
    if monitor_config:
        commands.extend(get_commands(event, monitor_config.exec_on_disconnect))
    return config, event, commands


def process(config, event):
    assert event and event.event and config

    commands = []

    if event.event == CONNECTED:
        _, _, commands = compose(set_wallpapers,
                                 activate_crtc)(config, event, [])
    elif event.event == DISCONNECTED:
        _, _, commands = deactivate_crtc(config, event, [])

    return functools.reduce(
        lambda r1, r2: r1 if r1 and r1 > 0 else r2,
        map(execute, commands))
        # map(jam(execute, print), commands))


def main():
    event = Event(
        output=os.environ.get('SRANDRD_OUTPUT', None),
        event=os.environ.get('SRANDRD_EVENT', None),
        edid=os.environ.get('SRANDRD_EDID', None),
        screenid=os.environ.get('SRANDRD_SCREENID', None)
    )
    global_config = GlobalConfiguration(
        outputs=get_connected_outputs(),
        monitors_config=toml.load(CONFIG_FILE),
        default_monitor=os.environ.get('SCREENCONFIG_DEFAULT',
                                       DEFAULT_MONITOR),
    )
    return process(global_config,  event)


if __name__ == "__main__":
    sys.exit(main())
