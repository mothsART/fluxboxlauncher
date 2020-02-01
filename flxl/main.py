import os
from os.path import dirname, join
import sys

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf

from .lib.desktop import get_info
from .lib.soft import Soft
from .lib.dialog import ConfirmDialog, WarningDialog, CmdLineDialog
from .lib.config import Conf
from .lib.i18n import (
    _duplicate, _app_already_exists,
    _confirmation, _confirm_question,
    _drag, _search, _activate,
    _add_cmd_line
)

def gtk_style():
    css = b"""
#drag-zone {
    background-color: white;
    border: dashed red 1px;
    margin: 20px;
}

#apps {
    border-bottom: solid grey 1px;
}
    """
    style_provider = Gtk.CssProvider()
    style_provider.load_from_data(css)

    Gtk.StyleContext.add_provider_for_screen(
        Gdk.Screen.get_default(),
        style_provider,
        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )


class FluxBoxLauncherWindow(Gtk.Window):
    ICONSIZE = 32

    def del_soft(self, conf, soft, hbox, vbox, hbox_header=None):
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
        if hbox_header and not conf.softs:
            vbox.remove(hbox_header)

    def on_checked(self, widget, soft, conf):
        if widget.get_active():
            soft.disabled = False
            conf.enable(soft)
        else:
            soft.disabled = True
            conf.disable(soft)
        conf.save()

    def _add_soft(self, conf, soft, vbox, hbox_header=None):
        if hbox_header and conf.softs:
            vbox.remove(hbox_header)
        hbox = Gtk.HBox(homogeneous=False, margin=5)

        delbtn = Gtk.Button(margin=5)
        deli = Gtk.Image()
        deli.set_from_stock(Gtk.STOCK_DELETE, Gtk.IconSize.MENU)
        delbtn.set_image(deli)
        delbtn.connect_object(
            "clicked",
            self.del_soft,
            conf,
            soft,
            hbox,
            vbox,
            hbox_header
        )
        img = Gtk.Image(margin=5)
        if (
            soft.icon != None
            and os.path.isfile(soft.icon)
            and (
                soft.icon.endswith('.png')
                or soft.icon.endswith('.jpg')
            )
        ):
            pixbuf = GdkPixbuf.Pixbuf.new_from_file(soft.icon)
            scaled_buf = pixbuf.scale_simple(
                self.ICONSIZE,
                self.ICONSIZE,
                GdkPixbuf.InterpType.BILINEAR
            )
            img.set_from_pixbuf(scaled_buf)
        elif soft.icon != None:
            img.set_from_icon_name(soft.icon, self.ICONSIZE)
            img.set_pixel_size(self.ICONSIZE)

        label = Gtk.Label(soft.name, margin=5)
        activateButton = Gtk.CheckButton(margin=5)
        activateButton.set_active(not soft.disabled)
        activateButton.connect(
            "toggled",
            self.on_checked,
            soft,
            conf
        )
        hbox.pack_start(delbtn, False, False, False)
        hbox.pack_start(img, False, False, False)
        hbox.pack_start(label, True, False, False)
        hbox.pack_start(activateButton, False, False, False)
        hbox.set_name('apps')
        vbox.pack_end(hbox, False, False, False)
        if hbox_header:
            vbox.pack_end(hbox_header, False, False, False)

    def on_drag_data_received(
        self, widget, context, x, y,
        selection, target_type, timestamp,
        conf, vbox, hbox_header
    ):
        data = selection.get_data().strip().replace(b'%20', b' ')
        f = data.replace(b"file://", b"").strip()
        if not os.path.isfile(f):
            return
        soft = Soft(*get_info(f))
        if conf.soft_exist(soft):
            confirmWarning = WarningDialog(
                self,
                _duplicate,
                _app_already_exists
            )
            confirmWarning.run()
            confirmWarning.destroy()
            return
        self._add_soft(conf, soft, vbox, hbox_header)
        vbox.show_all()
        conf.add(soft)
        conf.save()

    def appfinder(self, widget=None, event=None):
        os.system('rox /usr/share/applications &')

    def add_cmd(self, widget, event, conf, vbox, hbox_header):
        confirm = CmdLineDialog(
            self,
            _add_cmd_line
        )
        response = confirm.run()
        if not response == Gtk.ResponseType.OK:
            confirm.destroy()
            return
        cmd = confirm.entry.get_text().strip()
        soft = Soft(cmd, cmd)
        if conf.soft_exist(soft):
            confirmWarning = WarningDialog(
                self,
                _duplicate,
                _app_already_exists
            )
            confirmWarning.run()
            confirmWarning.destroy()
            confirm.destroy()
            self.add_cmd(widget, event, conf, vbox, hbox_header)
            return
        confirm.destroy()
        self._add_soft(conf, soft, vbox, hbox_header)
        vbox.show_all()
        conf.add(soft)
        conf.save()

    def __init__(self, conf):
        if conf.DEBUG:
            print('DEBUG MODE')
        Gtk.Window.__init__(
            self,
            title = 'Fluxbox Launcher'
        )
        conf.open()
        conf.save()

        self.set_border_width(5)

        vbox = Gtk.VBox(homogeneous=False)

        label = Gtk.Label(_activate, margin=5)
        hbox_header = Gtk.HBox(homogeneous=False)
        hbox_header.pack_end(label, False, False, False)
        
        TARGET_TYPE_URI_LIST = 80
        dnd_list = [ 
            Gtk.TargetEntry.new(
                'text/uri-list', 0, TARGET_TYPE_URI_LIST 
            )
        ]
        h = Gtk.HBox(homogeneous=False)
        h.set_name('drag-zone')
        h.drag_dest_set(
            Gtk.DestDefaults.ALL,
            dnd_list, 
            Gdk.DragAction.COPY
        )
        h.set_property("height-request", 200)
        h.connect(
            "drag-data-received",
            self.on_drag_data_received,
            conf, vbox, hbox_header
        )

        horizontal_header = Gtk.HBox(homogeneous=False)

        # add a shell cmd
        cmd_btn = Gtk.Button(
            label = ' ' + _add_cmd_line,
            margin=10
        )
        cmd_btn.connect(
            "button_press_event",
            self.add_cmd,
            conf, vbox, hbox_header
        )
        addi = Gtk.Image()
        addi.set_from_stock(Gtk.STOCK_ADD, Gtk.IconSize.MENU)
        cmd_btn.set_image(addi)
        horizontal_header.pack_start(cmd_btn, True, True, False)

        # search button
        appfinderbtn = Gtk.Button(
            label = ' ' + _search,
            margin=10
        )
        addi = Gtk.Image()
        addi.set_from_stock(Gtk.STOCK_FIND, Gtk.IconSize.MENU)
        appfinderbtn.set_image(addi)
        appfinderbtn.connect("button_press_event", self.appfinder)
        horizontal_header.pack_start(appfinderbtn, True, True, False)
        vbox.pack_start(horizontal_header, True, True, False)

        # drag and drop widget
        drag_vbox = Gtk.VBox(homogeneous=False)
        l = Gtk.Label(_drag)
        drag_vbox.pack_start(l, True, True, 10)
        appfinderbtn.show()
        l.show()
        h.pack_start(drag_vbox, True, True, False)
        vbox.pack_start(h, True, True, False)

        for soft in conf.softs:
            self._add_soft(conf, soft, vbox)

        # activate header
        if conf.softs:
            vbox.pack_end(hbox_header, False, False, False)

        swin = Gtk.ScrolledWindow()
        swin.add_with_viewport(vbox)
        self.add(swin)
        self.set_default_size(800, 600)
        self.show_all()


def main():
    user = None
    if len(sys.argv) > 1:
        user = sys.argv[1]
    gtk_style()
    win = FluxBoxLauncherWindow(Conf(user))
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
    exit(0)
