#!/usr/bin/env python
# coding: utf-8

'''Be happy with your clipboard.

Usage:
    ./cliptopia.py [options] [copy|paste|daemon|focused]

copy: Copy using Ctrl(+Shift)+c depending on window class.
paset: Paste using Ctrl(+Shift)+v depending on window class.
daemon: Start daemon to monitor clipboard changes.
focused: Return the id of current focused window.

Options:
    -h --help               Show this message.
'''

from docopt import docopt
from Xlib.display import Display

from keys import KeyHandler
from configs import SHIFTED_COPY_PASTE_CLASSES


display = Display()


def get_focused():
    '''Return currently focused window'''
    return display.get_input_focus().focus


def is_shifted(classes):
    '''Return True only if any of the classes is among the
    ones that should copy|paste with Ctrl+Shift+c|v'''
    for c in classes:
        if c in SHIFTED_COPY_PASTE_CLASSES:
            return True
    return False


def copy_from_focused():
    '''Copy text from focused window'''
    focus = get_focused()
    kh.copy(focus, is_shifted(focus.get_wm_class()))
    display.flush()


def paste_to_focused():
    '''Paste text to focused window'''
    focus = get_focused()
    kh.paste(focus, is_shifted(focus.get_wm_class()))
    display.flush()


def get_mouse_pos():
    '''Return current mouse position (x,y)'''
    data = display.screen().root.query_pointer()._data
    return data["root_x"], data["root_y"]


if __name__ == '__main__':
    arguments = docopt(__doc__)

    kh = KeyHandler(display)

    if arguments['copy']:
        # Copy from focused window
        copy_from_focused()
    elif arguments['paste']:
        # Paste to focused window
        paste_to_focused()
    elif arguments['focused']:
        # Print focused window id
        print(get_focused().id)
    elif arguments['daemon']:
        # Start daemon
        from clipboard import Clipboard
        Clipboard().run()
    elif arguments['history']:
        # print history?
        pass


# --------- Automate mouse clicks:
# import time
# from Xlib import X
# from Xlib.display import Display
# from Xlib.ext import xtest
# d=Display()
# def click(b):
#     xtest.fake_input(d.get_input_focus().focus, X.ButtonPress, b)
#     d.flush()
#     d.sync()
#     xtest.fake_input(d.get_input_focus().focus, X.ButtonRelease, b)
#     d.flush()
#     d.sync()
# time.sleep(2)
# [click(1) for i in range(20)]
# time.sleep(2); [click(1) for i in range(20)]
