# Cliptopia

**Be happy with your clipboard!** (really? well, maybe...)

This is a small group of scripts to help handle your clipboard.
They are aimed for people who uses X but like terminal applications.
**It only handle text clipboard entries.**

It handles selection 'CLIPBOARD' and 'PRIMARY' as one.
So what you copy with the mouse can be pasted with the keyboard and the other way round.

Tested only with Python 3.5.


These scripts were somehow inspired on [Clipit](https://github.com/shantzu/ClipIt) and [AutoKey](https://github.com/guoci/autokey-py3).

![Screenshot: show_history popup opened](https://raw.githubusercontent.com/andresmrm/cliptopia/master/img/example.png)

## Features

- Clipboard history daemon (accessible through dbus (is this safe?))
- Clipboard history display and selection (using [urwid](http://urwid.org))
- Smart copy&paste (automatically handling of `Ctrl+Shift+c|v` for terminals and `Ctrl+c|v` for other applications)

### Planned features

- Transcribe clipboard instead of using `Ctrl(+Shift)+v` (useful when `Ctrl(+Shift)+v` is not allowed).
- Paste snippets.
- Automate mouse clicks (like: press button1 ten times).

## Installation

Clone or copy this repository and install python dependencies listed in `requirements.txt`.
But `pygobject` and `dbus-python` seem not to be working with `pip`, so you'll have to install them with your distro package manager. =/

For Arch Linux that would be:

    # pacman python-gobject dbus-glib python-dbus
    
If you also want to install the other deps with package manager:
    
    # pacman python-docopt python-urwid
    
And, in Arch Linux, `python-xlib` for Python 3 is only in AUR.
One way to install it would be:

    # yaourt python-xlib
    
    
### More one dependency...

You'll also need to install `wmctrl` (it's a program, not a Python lib) for "smart focus" functionality (see below).

Again, in Arch Linux:

    # pacman wmctrl

## Usage

Still reading?
Ok, I'll tell how I use the scripts, so you can see if they are useful for you:

### Smart Copy&Paste

To avoid having to use `Ctrl+c` to copy a text from Firefox and `Ctrl+Shift+v` to paste it on terminal, the script handle that to me.
I have a system wide hotkey that calls `cliptopia.py copy` and another for `cliptopia.py paste`.
This 2 hotkeys will use `Ctrl+Shift+c|v` or `Ctrl+c|v` according to which window is on focus.

You need to configure which window classes should receive a `Ctrl+Shift+c|v` instead of just `Ctrl+c|v`.
See config section below.

### Clipboard History

For the history to be recorded a daemon must be running.
Start it with `cliptopia.py daemon`, stop it with (not implemented).

To display the history, call `show_history.py`.
It should open a terminal application.
Select an entry with arrow keys and `enter` or the hotkey in the start of the line.
Use `esc` to close without changing the current clipboard.
Example: Pressing `b` should set the clipboard for the previous entry. Pressing `c` would set it for the previous to the previous entry.
After selecting an entry, try pasting it with `Ctrl(+Shift)+v` or `cliptopia.py copy`.

To display the history in a "popup window", call `show_history.py --open-terminal`.
This should open a terminal window and display the clipboard history inside of it.
See configs section about how to set which terminal emulator and shell to use.

*`show_history.py` is only an example of an application to display clipboard history using Urwid (I like Urwid =) ). Other interfaces can be made (with GTK for example) using the same daemon provided here (`cliptopia.py daemon`), communicating through dbus.*

#### Smart Focus

When closing the history opened in a popup, sometimes the focus goes to a window different from the one you were editing previous to opening the popup.
To avoid that, `show_history --open-terminal` tries to change the focus back to the previous window using `wmctrl`, which must be installed for it to work.
If you don't want this behavior use `show_history --open-terminal --no-focus-change`.


## Configuration

Configuration must be done editing the `configs.py` file (really? yeah...).
It tries to guess configuration based on `$TERMINAL` and `$SHELL`, but it may not work...

Setting a custom title for the popup window you can later customize its behavior/appearance with the window manager (see example below).

### i3 configuration tips

I use [i3](https://i3wm.org), so I can give some extra tips configuring there.
Add the lines below to `~/.i3/config`. Don't forget to set things between `<>`.

    set $CLIPTOPIA_FOLDER <path cliptopia src folder>

    # start daemon
    exec python $CLIPTOPIA_FOLDER/cliptopia.py daemon
    # smart copy&paste
    bindsym --release <copy hotkey> exec --no-startup-id $CLIPTOPIA_FOLDER/cliptopia.py copy
    bindsym --release <paste hotkey> exec --no-startup-id $CLIPTOPIA_FOLDER/cliptopia.py paste
    # open history popup
    bindsym --release <show history hotkey> exec "$CLIPTOPIA_FOLDER/show_history.py --open-terminal"
    # set popup window to float (now a real popup!)
    for_window [title="cliptopia-popup"] floating enable
