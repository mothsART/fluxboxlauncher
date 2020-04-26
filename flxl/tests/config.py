from unittest import TestCase

from flxl.lib.config import Conf
from flxl.lib.soft import Soft

startup = """#!/bin/sh
#
# fluxbox startup-script:
#
# Lines starting with a '#' are ignored.

# Change your keymap:
# xmodmap "/home/primtux/.Xmodmap"

# Applications you want to run with fluxbox.
# MAKE SURE THAT APPS THAT KEEP RUNNING HAVE AN ''&'' AT THE END.
#
# unclutter -idle 2 &
# wmnd &
# wmsmixer -w &
# idesk &
#
# Debian-local change:
#   - fbautostart has been added with a quick hack to check to see if it
#     exists. If it does, we'll start it up by default.
which fbautostart > /dev/null
if [ $? -eq 0 ]; then
    fbautostart
fi

# And last but not least we start fluxbox.
# Because it is the last app you have to run it with ''exec'' before it.
exec /usr/lib/policykit-1-gnome/polkit-gnome-authentication-agent-1 &
exec xfce4-panel &
exec lxpanel &
exec rox -p 1 &
exec setxkbmap fr &
# exec /usr/bin/BNE-Linux &
# exec /usr/local/bin/primtux/handymenu-mini &
# exec /usr/local/bin/primtux/handymenu-super &
# exec /usr/local/bin/primtux/handymenu-maxi &
exec /usr/local/bin/primtux/accueil &
# exec xscreensaver -nosplash &
# exec /usr/local/bin/primtux/lanceurs &
exec fluxbox
# or if you want to keep a log:
# exec fluxbox -log "/home/primtux/.fluxbox/log
"""

startup_add = """#!/bin/sh
#
# fluxbox startup-script:
#
# Lines starting with a '#' are ignored.

# Change your keymap:
# xmodmap "/home/primtux/.Xmodmap"

# Applications you want to run with fluxbox.
# MAKE SURE THAT APPS THAT KEEP RUNNING HAVE AN ''&'' AT THE END.
#
# unclutter -idle 2 &
# wmnd &
# wmsmixer -w &
# idesk &
#
# Debian-local change:
#   - fbautostart has been added with a quick hack to check to see if it
#     exists. If it does, we'll start it up by default.
which fbautostart > /dev/null
if [ $? -eq 0 ]; then
    fbautostart
fi

# And last but not least we start fluxbox.
# Because it is the last app you have to run it with ''exec'' before it.
exec /usr/lib/policykit-1-gnome/polkit-gnome-authentication-agent-1 &
exec xfce4-panel &
exec lxpanel &
exec rox -p 1 &
exec setxkbmap fr &
# exec /usr/bin/BNE-Linux &
# exec /usr/local/bin/primtux/handymenu-mini &
# exec /usr/local/bin/primtux/handymenu-super &
# exec /usr/local/bin/primtux/handymenu-maxi &
exec /usr/local/bin/primtux/accueil &
# exec xscreensaver -nosplash &
# exec /usr/local/bin/primtux/lanceurs &
exec firefox &
exec fluxbox
# or if you want to keep a log:
# exec fluxbox -log "/home/primtux/.fluxbox/log
"""

startup_delete = """#!/bin/sh
#
# fluxbox startup-script:
#
# Lines starting with a '#' are ignored.

# Change your keymap:
# xmodmap "/home/primtux/.Xmodmap"

# Applications you want to run with fluxbox.
# MAKE SURE THAT APPS THAT KEEP RUNNING HAVE AN ''&'' AT THE END.
#
# unclutter -idle 2 &
# wmnd &
# wmsmixer -w &
# idesk &
#
# Debian-local change:
#   - fbautostart has been added with a quick hack to check to see if it
#     exists. If it does, we'll start it up by default.
which fbautostart > /dev/null
if [ $? -eq 0 ]; then
    fbautostart
fi

# And last but not least we start fluxbox.
# Because it is the last app you have to run it with ''exec'' before it.
exec /usr/lib/policykit-1-gnome/polkit-gnome-authentication-agent-1 &
exec xfce4-panel &
exec lxpanel &
exec rox -p 1 &
exec setxkbmap fr &
# exec /usr/bin/BNE-Linux &
# exec /usr/local/bin/primtux/handymenu-mini &
# exec /usr/local/bin/primtux/handymenu-super &
exec /usr/local/bin/primtux/accueil &
# exec xscreensaver -nosplash &
# exec /usr/local/bin/primtux/lanceurs &
exec fluxbox
# or if you want to keep a log:
# exec fluxbox -log "/home/primtux/.fluxbox/log
"""

after_disable = """#!/bin/sh
#
# fluxbox startup-script:
#
# Lines starting with a '#' are ignored.

# Change your keymap:
# xmodmap "/home/primtux/.Xmodmap"

# Applications you want to run with fluxbox.
# MAKE SURE THAT APPS THAT KEEP RUNNING HAVE AN ''&'' AT THE END.
#
# unclutter -idle 2 &
# wmnd &
# wmsmixer -w &
# idesk &
#
# Debian-local change:
#   - fbautostart has been added with a quick hack to check to see if it
#     exists. If it does, we'll start it up by default.
which fbautostart > /dev/null
if [ $? -eq 0 ]; then
    fbautostart
fi

# And last but not least we start fluxbox.
# Because it is the last app you have to run it with ''exec'' before it.
exec /usr/lib/policykit-1-gnome/polkit-gnome-authentication-agent-1 &
exec xfce4-panel &
# exec lxpanel &
# exec rox -p 1 &
exec setxkbmap fr &
# exec /usr/bin/BNE-Linux &
# exec /usr/local/bin/primtux/handymenu-mini &
# exec /usr/local/bin/primtux/handymenu-super &
# exec /usr/local/bin/primtux/handymenu-maxi &
exec /usr/local/bin/primtux/accueil &
# exec xscreensaver -nosplash &
# exec /usr/local/bin/primtux/lanceurs &
exec fluxbox
# or if you want to keep a log:
# exec fluxbox -log "/home/primtux/.fluxbox/log
"""

after_enable = """#!/bin/sh
#
# fluxbox startup-script:
#
# Lines starting with a '#' are ignored.

# Change your keymap:
# xmodmap "/home/primtux/.Xmodmap"

# Applications you want to run with fluxbox.
# MAKE SURE THAT APPS THAT KEEP RUNNING HAVE AN ''&'' AT THE END.
#
# unclutter -idle 2 &
# wmnd &
# wmsmixer -w &
# idesk &
#
# Debian-local change:
#   - fbautostart has been added with a quick hack to check to see if it
#     exists. If it does, we'll start it up by default.
which fbautostart > /dev/null
if [ $? -eq 0 ]; then
    fbautostart
fi

# And last but not least we start fluxbox.
# Because it is the last app you have to run it with ''exec'' before it.
exec /usr/lib/policykit-1-gnome/polkit-gnome-authentication-agent-1 &
exec xfce4-panel &
exec lxpanel &
exec rox -p 1 &
exec setxkbmap fr &
# exec /usr/bin/BNE-Linux &
exec /usr/local/bin/primtux/handymenu-mini &
# exec /usr/local/bin/primtux/handymenu-super &
# exec /usr/local/bin/primtux/handymenu-maxi &
exec /usr/local/bin/primtux/accueil &
# exec xscreensaver -nosplash &
# exec /usr/local/bin/primtux/lanceurs &
exec fluxbox
# or if you want to keep a log:
# exec fluxbox -log "/home/primtux/.fluxbox/log
"""


class TestConf(TestCase):
    def test_load(self):
        conf = Conf('primtux')
        lines = startup.split('\n')
        lines = [line + '\n' for line in lines]
        conf.load(lines[:-1])
        assert str(conf) == startup

    def test_add(self):
        conf = Conf('primtux')
        lines = startup.split('\n')
        lines = [line + '\n' for line in lines]
        conf.load(lines[:-1])
        soft = Soft('firefox', 'firefox', '', '')
        conf.add(soft)
        assert str(conf) == startup_add

    def test_remove(self):
        conf = Conf('primtux')
        lines = startup.split('\n')
        lines = [line + '\n' for line in lines]
        conf.load(lines[:-1])
        has_removed = conf.remove(
            conf.get_soft('/usr/local/bin/primtux/handymenu-maxi')
        )
        assert has_removed is True
        assert str(conf) == startup_delete

    def test_disable(self):
        conf = Conf('primtux')
        lines = startup.split('\n')
        lines = [line + '\n' for line in lines]
        conf.load(lines[:-1])
        soft = conf.get_soft('rox -p 1')
        conf.disable(soft)
        soft = conf.get_soft('lxpanel')
        conf.disable(soft)
        assert str(conf) == after_disable

    def test_enable(self):
        conf = Conf('primtux')
        lines = startup.split('\n')
        lines = [line + '\n' for line in lines]
        conf.load(lines[:-1])
        soft = conf.get_soft('/usr/local/bin/primtux/handymenu-mini')
        conf.enable(soft)
        assert str(conf) == after_enable
