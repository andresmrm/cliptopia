#!/usr/bin/env python
# coding: utf-8

import os


# Guess default configs base on ENV vars.
terminal = os.environ['TERMINAL']
shell = os.environ['SHELL']


# Window classes which should copy&paste with Ctrl+Shift+c/v
# instead of Shift+c/v.
# You can use a program like 'xprop' to find out the class of
# windows.
# Try to guess window class based on the name of used terminal.
SHIFTED_COPY_PASTE_CLASSES = [terminal]


# Set here a command to open a terminal and execute the script there
# each argument of the terminal should be an item of the list.
# The {command} part will be replaced with the command that should be run.
# Some terminals allow a '-t' parameter to set the window title, this can
# be used to customize window behavior in the window manager (like setting)
# it to floating.
# Value examples:
# ['termite', '-e', 'zsh -c "{command}"']
# ['urxvt', '-e', 'bash -c "{command}"']
OPEN_TERMINAL = [terminal, '-t', 'cliptopia-popup', '-e',
                 shell + ' -c "{command}"']


# Maximum number of stored clipboard history entries.
HISTORY_MAX_SIZE = 50
