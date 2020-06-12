#!/usr/bin/env python3.8

# (C) DAVIDhaker, 2020
# E-Mail: DAVIDhaker@yandex.ru

import re
import dbus.service
import json

from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib

DBusGMainLoop(set_as_default=True)

db = json.load(open('db.json'))

session_bus = dbus.SessionBus()

def get_mac_info(prefix):
    try:
        return db[prefix.upper()]
    except KeyError:
        return None


class Runner(dbus.service.Object):
    def __init__(self):
        super().__init__(dbus.service.BusName('net.test2', session_bus), '/krunner_mac_plugin')

    @dbus.service.method('org.kde.krunner1', in_signature='s', out_signature='a(sssida{sv})')
    def Match(self, query: str):
        """
        If entered a valid MAC: Format it into all available formats and try to detect country
        return it to KRunner
        """

        if not re.match('^((([0-9a-f]{2}(:|-)){5}[0-9a-f]{2})|([0-9a-f]{4}\.){2}[0-9a-f]{4})$', query, flags=re.IGNORECASE):
            return []

        cleaned_mac = query.replace('-', '').replace('.', '').replace(':', '').upper()

        info = get_mac_info(cleaned_mac[0:6])

        by2 = re.findall('..', cleaned_mac)
        by4 = re.findall('....', cleaned_mac)

        result = []

        i = .8

        if info:
            info = f"{info['company']} ({info['country']})"

            result.append([info, info, "routeplanning", 100, 0.10, {'subtext': 'Company'}])

        result += [
            (f"{mac}", mac, "edit-copy", 100, (i := i - .1), {'subtext': 'Copy'}) for mac in [
            ':'.join(by2).lower(), # xx:xx:xx:xx:xx
            ':'.join(by2).upper(), # XX:XX:XX:XX:XX
            '-'.join(by2).lower(), # xx-xx-xx-xx-xx
            '-'.join(by2).upper(), # XX-XX-XX-XX-XX
            '.'.join(by4).lower(), # xxxx.xxxx.xxxx
            '.'.join(by4).upper(), # XXXX.XXXX.XXXX
            ]
        ]

        return result

    @dbus.service.method('org.kde.krunner1', in_signature='ss')
    def Run(self, data: str, _action_id: str):
        """
        On any command copy to the KRunner query field
        """
        session_bus.call_blocking(
            bus_name='org.kde.krunner',
            object_path='/App',
            dbus_interface='org.kde.krunner.App',
            method='query',
            signature='s',
            args=[data]
        )

runner = Runner()
loop = GLib.MainLoop()
loop.run()
