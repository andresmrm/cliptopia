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
    return display.get_input_focus().focus


def is_shifted(classes):
    for c in classes:
        if c in SHIFTED_COPY_PASTE_CLASSES:
            return True
    return False


def copy_from_focused():
    focus = get_focused()
    kh.copy(focus, is_shifted(focus.get_wm_class()))
    display.flush()


def paste_to_focused():
    focus = get_focused()
    kh.paste(focus, is_shifted(focus.get_wm_class()))
    display.flush()


def get_mouse_pos():
    data = display.screen().root.query_pointer()._data
    return data["root_x"], data["root_y"]


if __name__ == '__main__':
    arguments = docopt(__doc__)

    kh = KeyHandler(display)

    if arguments['copy']:
        copy_from_focused()
    elif arguments['paste']:
        paste_to_focused()
    elif arguments['focused']:
        print(get_focused().id)
    elif arguments['daemon']:
        import clipboard
        clipboard.Manager().run()
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
