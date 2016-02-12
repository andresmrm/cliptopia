#!/usr/bin/env python
# coding: utf-8

import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop

from consts import SERVICE_NAME, SERVICE_PATH


class DBUSService(dbus.service.Object):

    def __init__(self, manager):
        self.manager = manager
        bus_name = dbus.service.BusName(SERVICE_NAME, bus=dbus.SessionBus())
        dbus.service.Object.__init__(self, bus_name, SERVICE_PATH)

    @dbus.service.method(SERVICE_NAME)
    def get_history(self):
        '''Return entire clipboard history'''
        h = self.manager.get_history()
        return h if h else ''

    @dbus.service.method(SERVICE_NAME)
    def set_clipboard(self, text):
        '''Set current clipboard to text'''
        self.manager.set_clipboard(text)


def init_dbus_service(manager):
    '''Prepare to listen to DBUS'''
    DBusGMainLoop(set_as_default=True)
    DBUSService(manager)
