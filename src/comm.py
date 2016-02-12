#!/usr/bin/env python
# coding: utf-8

import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop

from consts import SERVICE_NAME, SERVICE_PATH


class MyDBUSService(dbus.service.Object):

    def __init__(self, manager):
        self.manager = manager
        bus_name = dbus.service.BusName(SERVICE_NAME, bus=dbus.SessionBus())
        dbus.service.Object.__init__(self, bus_name, SERVICE_PATH)

    @dbus.service.method(SERVICE_NAME)
    def get_history(self):
        h = self.manager.get_history()
        return h if h else ''

    @dbus.service.method(SERVICE_NAME)
    def set_clipboard(self, text):
        h = self.manager.set_clipboard(text)
        return h if h else ''


def init_dbus_service(manager):
    DBusGMainLoop(set_as_default=True)
    MyDBUSService(manager)
