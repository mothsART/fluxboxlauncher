import os
from os.path import join

import gi
gi.require_version('Gdk', '3.0')  # noqa E402
gi.require_version('Gtk', '3.0')  # noqa E402
from gi.repository import Gtk, Gdk, GdkPixbuf

from .lib.style import gtk_style
from .lib.utils import new_img
from .lib.desktop import get_info
from .lib.soft import Soft
from .lib.dialog import ConfirmDialog, WarningDialog, CmdLineDialog
from .lib.config import Conf, UserConf
from .lib.i18n import (
    _duplicate, _app_already_exists,
    _confirmation, _confirm_question,
    _drag, _search, _activate,
    _add_cmd_line
)

class FluxBoxLauncherWindow(Gtk.Window):
    ICONSIZE = 32

    def del_soft(self, user_conf, soft, hbox, vbox, hbox_header=None):
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
        user_conf.remove(soft)
        user_conf.save()
        vbox.remove(hbox)
        if hbox_header and not user_conf.softs:
            vbox.remove(hbox_header)

    def on_checked(self, widget, soft, user_conf):
        if widget.get_active():
            soft.disabled = False
            user_conf.enable(soft)
        else:
            soft.disabled = True
            user_conf.disable(soft)
        user_conf.save()

    def _add_soft(self, user_conf, soft, vbox, hbox_header=None):
        if hbox_header and user_conf.softs:
            vbox.remove(hbox_header)
        hbox = Gtk.HBox(homogeneous=False, margin=5)

        delbtn = Gtk.Button(margin=5)
        deli = Gtk.Image()
        deli.set_from_stock(Gtk.STOCK_DELETE, Gtk.IconSize.MENU)
        delbtn.set_image(deli)
        delbtn.connect_object(
            'clicked',
            self.del_soft,
            user_conf,
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
            'toggled',
            self.on_checked,
            soft,
            user_conf
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
        user_conf, vbox, hbox_header
    ):
        data = selection.get_data().strip().replace(b'%20', b' ')
        f = data.replace(b'file://', b'').strip()
        if not os.path.isfile(f):
            return
        soft = Soft(*get_info(f))
        if user_conf.soft_exist(soft):
            confirmWarning = WarningDialog(
                self,
                _duplicate,
                _app_already_exists
            )
            confirmWarning.run()
            confirmWarning.destroy()
            return
        self._add_soft(user_conf, soft, vbox, hbox_header)
        vbox.show_all()
        user_conf.add(soft)
        user_conf.save()

    def appfinder(self, widget, event, user_conf, vbox, hbox_header):
        dialog = Gtk.AppChooserDialog(
            parent=self,
            content_type='image/png'
        )
        dialog.set_heading(_search)
        dialog.connect('response', self.on_response, user_conf, vbox, hbox_header)
        dialog.run()

    def on_response(self, dialog, response, user_conf, vbox, hbox_header):
        if response != Gtk.ResponseType.OK:
            dialog.destroy()
            return
        app_info = dialog.get_app_info()

        name = app_info.get_display_name()
        generic = app_info.get_generic_name()
        description = app_info.get_description()

        soft = Soft(*get_info(app_info.get_filename()))
        if user_conf.soft_exist(soft):
            dialog.destroy()
            confirmWarning = WarningDialog(
                self,
                _duplicate,
                _app_already_exists
            )
            confirmWarning.run()
            confirmWarning.destroy()
            return
        self._add_soft(user_conf, soft, vbox, hbox_header)
        vbox.show_all()
        user_conf.add(soft)
        user_conf.save()
        dialog.destroy()
        
    def add_cmd(self, widget, event, user_conf, vbox, hbox_header):
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
        if user_conf.soft_exist(soft):
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
        user_conf.add(soft)
        user_conf.save()

    def _create_tab(self, user, debug):
        user_conf = UserConf(user, debug)
        user_conf.open()
        user_conf.save()

        label = Gtk.Label(f'session : {user}')
        hbox = Gtk.HBox()
        img = new_img(user_conf.icon_path)
        if img:
            img_context = img.get_style_context()
            img_context.add_class('icon')
            hbox.pack_start(img, False, True, 0)
        hbox.pack_end(label, True, True, 0)
        hbox.show_all()

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
        h.set_property('height-request', 200)
        h.connect(
            'drag-data-received',
            self.on_drag_data_received,
            user_conf, vbox, hbox_header
        )

        horizontal_header = Gtk.HBox(homogeneous=False)

        # add a shell cmd
        cmd_btn = Gtk.Button(
            label = ' ' + _add_cmd_line,
            margin=10
        )
        cmd_btn.connect(
            'button_press_event',
            self.add_cmd,
            user_conf, vbox, hbox_header
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
        appfinderbtn.connect(
            'button_press_event',
            self.appfinder,
            user_conf, vbox, hbox_header
        )
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

        for soft in user_conf.softs:
            self._add_soft(user_conf, soft, vbox)

        # activate header
        if user_conf.softs:
            vbox.pack_end(hbox_header, False, False, False)

        swin = Gtk.ScrolledWindow()
        swin.add_with_viewport(vbox)
        
        return swin, hbox

    def __init__(self, conf):
        if conf.DEBUG:
            print('DEBUG MODE')
        Gtk.Window.__init__(
            self,
            title = 'Fluxbox Launcher'
        )
        self.set_border_width(5)
        notebook = Gtk.Notebook()
        notebook.set_tab_pos(Gtk.PositionType.TOP)

        for user in conf.users:
            swin, hbox = self._create_tab(user, conf.DEBUG)
            notebook.append_page(swin, hbox)

        self.add(notebook)
        self.set_default_size(800, 600)
        self.show_all()


def main():
    gtk_style()
    win = FluxBoxLauncherWindow(Conf())
    win.connect('destroy', Gtk.main_quit)
    win.show_all()
    Gtk.main()
    exit(0)
