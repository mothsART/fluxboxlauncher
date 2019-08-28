#!/usr/bin/python
# -*- coding:Utf-8 -*- 

import os
from os.path import dirname, join
import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

from lib.desktop import get_info
from lib.soft import Soft
from lib.dialog import ConfirmDialog, WarningDialog
from lib.config import Conf
from lib.i18n import (
    _duplicate, _app_already_exists,
    _confirmation, _confirm_question,
    _drag, _search
)


class FluxBoxLauncherWindow(Gtk.Window):
    ICONSIZE = 32

    def del_soft(self, conf, soft, hbox, vbox):
        confirm = ConfirmDialog(
            self,
            _confirmation,
            _confirm_question
        )
        response = confirm.run()
        if not response == Gtk.ResponseType.OK:
            confirm.destroy()
            return
        confirm.destroy()
        conf.remove(soft)
        conf.save()
        vbox.remove(hbox)

    def on_checked(self, widget, soft, conf):
        if widget.get_active():
            soft.disabled = False
            conf.enable(soft)
        else:
            soft.disabled = True
            conf.disable(soft)
        conf.save()

    def _add_soft(self, conf, soft, vbox):
        hbox = Gtk.HBox(homogeneous=False)

        delbtn = Gtk.Button()
        deli = Gtk.Image()
        deli.set_from_stock(Gtk.STOCK_DELETE, Gtk.IconSize.MENU)
        delbtn.set_image(deli)
        delbtn.connect_object(
            "clicked",
            self.del_soft,
            conf,
            soft,
            hbox,
            vbox
        )

        img = Gtk.Image()
        if (
            soft.icon != None
            and os.path.isfile(soft.icon)
            and (
                soft.icon.endswith('.png')
                or soft.icon.endswith('.jpg')
            )
        ):
            pixbuf = Gtk.gdk.pixbuf_new_from_file_at_size(
                soft.icon,
                self.ICONSIZE, self.ICONSIZE
            )
            scaled_buf = pixbuf.scale_simple(
                self.ICONSIZE, self.ICONSIZE,
                Gtk.gdk.INTERP_BILINEAR
            )
            img.set_from_pixbuf(scaled_buf)
        elif soft.icon != None:
            img.set_from_icon_name(soft.icon, self.ICONSIZE)
            img.set_pixel_size(self.ICONSIZE)

        label = Gtk.Label(soft.name)
        activateButton = Gtk.CheckButton()
        activateButton.set_active(not soft.disabled)
        activateButton.connect(
            "toggled",
            self.on_checked,
            soft,
            conf
        )
        activateButton.set_tooltip_text("actif ?")
        hbox.pack_start(delbtn, False, False, False)
        hbox.pack_start(img, False, False, False)
        hbox.pack_start(label, True,  False, False)
        hbox.pack_start(activateButton, False, False, False)

        vbox.pack_end(hbox, False, False, False)

    def on_drag_data_received(
        self, widget, context, x, y,
        selection, target_type, timestamp,
        conf, vbox
    ):
        data = selection.get_data().strip().replace('%20', ' ')
        f = data.replace("file://", "").strip()
        if not os.path.isfile(f):
            return
        soft = Soft(*get_info(f))

        if conf.soft_exist(soft):
            confirm = WarningDialog(
                self,
                _duplicate,
                _app_already_exists
            )
            confirm.run()
            confirm.destroy()
            return
        self._add_soft(conf, soft, vbox)
        vbox.show_all()
        conf.add(soft)
        conf.save()
        self._add_soft(conf, soft, vbox)

    def appfinder(self, widget=None, event=None):
        os.system('rox /usr/share/applications &')

    def __init__(self, conf):
        if conf.DEBUG:
            print('DEBUG MODE')
        Gtk.Window.__init__(
            self,
            title = 'Fluxbox Launcher'
        )
        self.set_border_width(5)

        vbox = Gtk.VBox(homogeneous=False)
        
        TARGET_TYPE_URI_LIST = 80
        dnd_list = [ 
            Gtk.TargetEntry.new(
                'text/uri-list', 0, TARGET_TYPE_URI_LIST 
            )
        ]
        h = Gtk.HBox(homogeneous=False)
        h.drag_dest_set(
            Gtk.DestDefaults.ALL,
            dnd_list, 
            Gdk.DragAction.COPY
        )
        h.connect(
            "drag-data-received",
            self.on_drag_data_received,
            conf, vbox
        )
        l = Gtk.Label(_drag)
        drag_vbox = Gtk.VBox(homogeneous=False)
        appfinderbtn = Gtk.Button(
            label = _search
        )
        appfinderbtn.connect("button_press_event", self.appfinder)
        drag_vbox.pack_start(appfinderbtn, False, False, 10)
        drag_vbox.pack_start(l, True, True, 10)
        appfinderbtn.show()
        l.show()
        h.pack_start(drag_vbox, True, True, False)
        vbox.pack_start(h, True, True, False)

        conf.open()
        conf.save()

        for soft in conf.softs:
            self._add_soft(conf, soft, vbox)
        label = Gtk.Label("activé ?")
        hbox = Gtk.HBox(homogeneous=False)
        hbox.pack_end(label, False, False, False)
        vbox.pack_end(hbox, False, False, False)
        
        swin = Gtk.ScrolledWindow()
        swin.add_with_viewport(vbox)
        self.add(swin)
        self.set_default_size(800, 600)
        self.show_all()


if __name__ == "__main__":
    user = None
    if len(sys.argv) > 1:
        user = sys.argv[1]
    win = FluxBoxLauncherWindow(Conf(user))
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
    exit(0)
