#!/usr/bin/env python
# coding: utf-8

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

import comm
from configs import HISTORY_MAX_SIZE


class Manager():

    def __init__(self):
        self.clip_keyboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        self.clip_mouse = Gtk.Clipboard.get(Gdk.SELECTION_PRIMARY)
        self.last_text = None
        self.history = History()

    def get_history(self):
        return self.history.get()

    def clip_changed(self, clip, void):
        Gdk.threads_enter()
        text = clip.wait_for_text()
        Gdk.threads_leave()
        if text is not None:

            changed = False
            Gdk.threads_enter()
            if text != self.last_text:
                self.last_text = text
                changed = True
                if changed:
                    print(text)
                    self.set_clipboard(text, str(void.selection), True)
                    # void.selection_time
                    self.history.add(text)
            Gdk.threads_leave()
        # else:
        #     raise Exception("No text found in X selection")

    def set_clipboard(self, text, selection_type=None, protected=False):
        if not protected:
            Gdk.threads_enter()
        if selection_type != 'CLIPBOARD':
            self.clip_keyboard.set_text(text, -1)
        if selection_type != 'PRIMARY':
            self.clip_mouse.set_text(text, -1)
        if not protected:
            Gdk.threads_leave()

    def connect_to_clipboard_signals(self):
        self.clip_keyboard.connect('owner-change', self.clip_changed)
        self.clip_mouse.connect('owner-change', self.clip_changed)

    def run(self):
        self.connect_to_clipboard_signals()
        print('starting cliptopia daemon')

        comm.init_dbus_service(self)
        # m = comm.MyObject()
        # m.connect('my_signal', print)

        # Gtk.main()

        from gi.repository import GLib
        GLib.MainLoop().run()

        # from gi.repository import GObject
        # GObject.MainLoop().run()

        # import urwid
        # txt = urwid.Text(u"Hello World")
        # fill = urwid.Filler(txt, 'top')
        # loop = urwid.MainLoop(fill, event_loop=urwid.GLibEventLoop())
        # loop.run()


class History():

    def __init__(self):
        self.history = []
        self.maxsize = HISTORY_MAX_SIZE

    def add(self, data):
        # Keep only one instance of each value
        try:
            self.history.remove(data)
        except ValueError:
            pass

        # Add new value
        self.history.append(data)

        # Keep list at maxsize
        if len(self.history) > self.maxsize:
            self.history.pop(0)

    def get(self):
        return self.history
