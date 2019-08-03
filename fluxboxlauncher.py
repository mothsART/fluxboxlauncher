#!/usr/bin/python
# -*- coding:Utf-8 -*- 

import os
from os.path import dirname, join
import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import toml

from lib.desktop import get_info
from lib.dialog import ConfirmDialog, WarningDialog
from lib.config import Conf
from lib.soft import Soft
from lib.i18n import (
    _confirmation, _confirm_question,
    _drag, _search
)

class FluxBoxLauncherWindow(Gtk.Window):
    ICONSIZE = 32
    softs    = []

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
        self.softs.remove(soft)
        new_toml = {}
        inc = 0
        start_stream = []
        for s in self.softs:
            inc = inc + 1
            if s.disabled:
                start_stream.append('# exec %s &\n' % s.cmd)
            else:
                start_stream.append('exec %s &\n' % s.cmd)
            new_toml = dict(
                new_toml,
                **s.to_dict(inc)
            )
        conf.update(start_stream, new_toml)
        vbox.remove(hbox)

    def on_checked(self, widget, soft, conf):
        soft.disabled = True
        if widget.get_active():
            soft.disabled = False
        start_stream = []
        inc          = 0
        new_toml     = {}
        for s in self.softs:
            inc = inc + 1
            if s.disabled:
                start_stream.append('# exec %s &\n' % s.cmd)
            else:
                start_stream.append('exec %s &\n' % s.cmd)
            new_toml = dict(
                new_toml, 
                **s.to_dict(inc)
            )
        conf.update(start_stream, new_toml)

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
            and (icon.endswith('.png') or icon.endswith('.jpg'))
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

        hbox.pack_start(delbtn, False, False, False)
        hbox.pack_start(img,    False, False, False)
        hbox.pack_start(label,  True,  False, False)
        hbox.pack_start(activateButton, False, False, False)

        vbox.pack_end(hbox,     False, False, False)

        self.softs.append(soft)

    def on_drag_data_received(
        self, widget, context, x, y,
        selection, target_type, timestamp,
        conf, vbox
    ):
        data = selection.get_data().strip().replace('%20', ' ')
        f = data.replace("file://", "").strip()
        if not os.path.isfile(f):
            return
        soft = Soft()
        soft.new(*get_info(f))
        for s in self.softs:
            if soft.cmd == s.cmd:
                confirm = WarningDialog(
                    self,
                    _('Duplicate'),
                    _('This application already exists')
                )
                confirm.run()
                confirm.destroy()
                return
        self._add_soft(conf, soft, vbox)
        vbox.show_all()
        start_stream = []
        for s in self.softs:
            if s.disabled:
                start_stream.append('# exec %s &\n' % s.cmd)
                continue
            start_stream.append('exec %s &\n' % s.cmd)
        conf.update(
            start_stream,
            soft.to_dict(len(self.softs))
        )
        #with open(conf.toml_path, 'a+') as f:
        #    f.write(
        #        ' \n'
        #        + toml.dumps(soft.to_dict(len(self.softs)))
        #    )

    def appfinder(self, widget=None, event=None):
        os.system('rox /usr/share/applications &')

    def load(self, conf, vbox):
        start_stream  = []
        self.cmd_list = []
        new_toml      = {}
        if not os.path.isfile(conf.toml_path):
            return start_stream, new_toml
        with open(conf.toml_path, 'r') as d:
            try:
                parsed_toml = toml.loads(d.read())
            except:
                print(
                    _(
                        '{0} is not a proper TOML file.'
                    ).format(conf.toml_path)
                )
                return start_stream, new_toml
        if len(parsed_toml) == 0:
            return start_stream, new_toml
        def sort_softs(soft):
            return int(soft.replace('soft-', ''))
        for soft_index in sorted(parsed_toml, key=sort_softs):
            soft_conf = parsed_toml[soft_index]
            if 'cmd' not in soft_conf:
                continue
            if soft_conf['cmd'] in self.cmd_list:
                continue
            soft = Soft()
            soft.cmd = soft_conf['cmd']
            self.cmd_list.append(soft.cmd)
            if 'name' in soft_conf:
                soft.name = soft_conf['name']
            if 'icon' in soft_conf:
                soft.icon = soft_conf['icon']
            if 'generic' in soft_conf:
                soft.generic = soft_conf['generic']
            if 'disabled' in soft_conf:
                soft.disabled = soft_conf['disabled']
            self._add_soft(conf, soft, vbox)
            if soft.disabled:
                start_stream.append('# exec %s &\n' % soft.cmd)
            else:
                start_stream.append('exec %s &\n' % soft.cmd)
            new_toml = dict(
                new_toml, 
                **soft.to_dict(len(self.softs))
            )
        return start_stream, new_toml

    def __init__(self, conf):
        if conf.DEBUG:
            print('DEBUG MODE')
        Gtk.Window.__init__(
            self,
            title = 'Fluxbox Launcher'
        )
        self.set_border_width(0)

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

        start_stream, new_toml = self.load(conf, vbox)
        conf.save(start_stream, new_toml)
        if start_stream == []:
            self.load(conf, vbox)

        swin = Gtk.ScrolledWindow()
        swin.add_with_viewport(vbox)
        self.add(swin)
        self.set_default_size(500, 600)
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
