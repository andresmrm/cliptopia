#!/usr/bin/env python
# coding: utf-8

'''Display clipboard history. Cliptopia daemon must be running.

Usage:
    ./show_history.py [options] [<focus-to>]

focus-to: The id of the window to change focus to when closing history.
          When -o is set, but not -n, this parameter will be used to
          try to go back the focus to the window that had focus before
          the popup openned. The program 'wmctrl' is required.
          E.g.:
          - Windows A, B and C are on the screen.
          - You are editing window B.
          - You use a hotkey to call this script with option -o.
          - A window D apears with the history, focus goes to it.
          - You pick an item, D closes, focus goes back to B.

Options:
    -h --help               Show this message.
    -o --open-terminal      Open a terminal and display the history
                            there (like a popup).
    -n --no-focus-change    Avoid trying to change focus back to
                            previous window when -o is set.
'''

import os
import string
import subprocess

import dbus
import urwid
from docopt import docopt

from consts import SERVICE_NAME, SERVICE_PATH
from configs import OPEN_TERMINAL


class ButtonClean(urwid.Button):
    '''Urwid button without < >'''
    button_left = urwid.Text('')
    button_right = urwid.Text('')


class Cui(object):

    def __init__(self, window):
        self.go_to_window = window
        self.setup_service()
        self.setup_history()
        self.hot_items = {}
        if not self.history:
            # No history to show...
            self.text_msg = urwid.Text('Empty history...')
            self.pile = urwid.Pile([
                (1, urwid.Filler(self.text_msg)),
            ])
            self.root = self.pile
        else:
            # Prepare history buttons list
            self.list_items()
            self.list_focus = urwid.SimpleFocusListWalker(self.items)
            self.list_box = urwid.ListBox(self.list_focus)
            self.root = self.list_box

        palette = [
            ('reversed', 'standout', '', 'bold'),
            ('bold', 'default,bold', 'default', 'bold'),
            ('reversed-bold', 'standout,bold', '', 'bold'),
        ]
        self.main = urwid.MainLoop(
            self.root,
            palette=palette,
            unhandled_input=self.hotkeys
        )
        self.main.run()

    def setup_service(self):
        bus = dbus.SessionBus()
        self.service = bus.get_object(SERVICE_NAME, SERVICE_PATH)

    def setup_history(self):
        method = self.service.get_dbus_method('get_history', SERVICE_NAME)
        self.history = method()

    def set_clipboard(self, text):
        method = self.service.get_dbus_method('set_clipboard', SERVICE_NAME)
        return method(text)

    def list_items(self):
        self.items = []
        symbols = self.generate_symbols()
        self.hot_items = {}
        for i in reversed(self.history):
            button = ButtonClean(i)
            urwid.connect_signal(button, 'click', self.item_chosen)
            b = urwid.AttrMap(button, 'bold', focus_map='reversed-bold')
            if symbols:
                s = symbols.pop(0)
                self.hot_items[s] = button
                t = urwid.Text(s)
            else:
                t = urwid.Text('-')
            self.items.append(urwid.Columns([(2, t), b]))
        # self.main.draw_screen()

    def generate_symbols(self):
        return [i for i in string.ascii_letters + string.digits]
        # self.symbols = string.punctuation
        # self.symbols = string.printable

    def hotkeys(self, key):
        hot_item = self.hot_items.get(key)
        if hot_item:
            urwid.emit_signal(hot_item, 'click', hot_item)
        elif key in ('esc',):
            self.close()

    def item_chosen(self, button):
        text = button.get_label()
        self.set_clipboard(text)
        self.close()

    def close(self):
        # TODO: use Xlib?
        if self.go_to_window:
            subprocess.call(('wmctrl -ia %s' % int(self.go_to_window)).split())
        raise urwid.ExitMainLoop()


if __name__ == '__main__':
    arguments = docopt(__doc__)
    focus_to = arguments['<focus-to>']
    if arguments['--open-terminal']:
        if not focus_to and not arguments['--no-focus-change']:
            import cliptopia
            myself = os.path.abspath(__file__)
            focus_to = cliptopia.get_focused().id
        OPEN_TERMINAL[-1] = OPEN_TERMINAL[-1].format(
            command="%s %s" % (myself, focus_to))
        subprocess.call(OPEN_TERMINAL)
    else:
        Cui(focus_to)
