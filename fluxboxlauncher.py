#!/usr/bin/python
# -*- coding:Utf-8 -*- 

import os
from os.path import dirname, join
import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import gettext
import locale
import toml

local_path = join(dirname(dirname(__file__)),  'locale')
gettext.bindtextdomain('fluxboxlauncher', local_path)
gettext.textdomain('fluxboxlauncher')
_ = gettext.gettext


def get_info_desktop(desktopfile):
    """return infos from a .desktop file"""
    name, cmd, icon, generic= "", "", "", ""
    nameloc = False
    geneloc = False
    lang = locale.setlocale(locale.LC_ALL, "")[0:2]
    with open(desktopfile,'r') as d:
        df = d.readlines()
    for l in df:
        if generic == "" or geneloc == False:
            if l.startswith('GenericName[{0}]='.format(lang)):
                generic = l.replace(
                    'GenericName[{0}]='.format(lang),''
                ).strip()
                geneloc = True
            elif l.startswith('GenericName='.format(lang)):
                generic = l.replace(
                    'GenericName='.format(lang),''
                ).strip()
        if name == "" or nameloc == False:
            if l.startswith('Name[{0}]='.format(lang)):
                name = l.replace(
                    'Name[{0}]='.format(lang),''
                ).strip()
                nameloc = True
            elif l.startswith('Name='):
                name = l.replace('Name=', '').strip()
        if cmd == "" and l.startswith('Exec='):
            cmd = l.replace('Exec=', '').strip()
            cmd = cmd.split('%')[0].strip()
        if icon == "" and l.startswith('Icon='):
            icon = os.path.splitext(
                l.replace('Icon=', '').strip()
            )[0]
    return name, cmd, icon, generic


def update_startup_file(start_path, start_stream):
    with open(start_path, 'r') as f:
       lines = f.readlines()
    first_lines = []
    final_lines = []
    after_fluxbox = False
    for line in lines:
        if after_fluxbox or line.startswith('exec fluxbox'):
            final_lines.append(line)
            after_fluxbox = True
            continue
        if line.startswith('exec '):
            continue
        if line.startswith('# exec '):
            continue
        first_lines.append(line)
    with open(start_path, 'w') as f:
        f.write(''.join(
            first_lines[:-1] + start_stream + ['\n'] + final_lines)
        )


class Conf:
    def __init__(self, user):
        self.DEBUG = False
        self.toml_path = 'start.toml'
        self.start_path = 'startup'
        if os.path.isdir('.git'):
            self.DEBUG = True
        dirname = "/home/%s/.fluxbox/" % user
        if not os.path.isdir(dirname):
            return
        self.toml_path  = dirname + 'start.toml'
        self.start_path = dirname + 'startup'


class Soft:
    name    = None
    cmd     = None
    icon    = None
    generic = None

    def __init__(self):
        pass

    def new(self, name, cmd, icon, generic):
        self.name    = name
        self.cmd     = cmd
        self.icon    = icon
        self.generic = generic
    
    def to_dict(self, inc):
        soft_title = 'soft-%s' % inc
        dic = {
            soft_title: {
                'name':    self.name,
                'cmd':     self.cmd
            }
        }
        if self.icon:
            dic[soft_title]['icon'] = self.icon
        if self.generic:
            dic[soft_title]['generic'] = self.generic
        return dic


class ConfirmDialog(Gtk.Dialog):

    def __init__(self, parent, title, message):
        Gtk.Dialog.__init__(
            self, title, parent, 0,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OK, Gtk.ResponseType.OK)
        )

        self.set_default_size(150, 100)
        box = self.get_content_area()
        if message:
            label = Gtk.Label(message)
            box.add(label)
        self.show_all()


class WarningDialog(Gtk.Dialog):

    def __init__(self, parent, title, message):
        Gtk.Dialog.__init__(
            self, title, parent, 0,
            (Gtk.STOCK_OK, Gtk.ResponseType.CANCEL)
        )

        self.set_default_size(100, 50)
        box = self.get_content_area()
        if message:
            label = Gtk.Label(message)
            box.add(label)
        self.show_all()


class FluxBoxLauncherWindow(Gtk.Window):
    ICONSIZE = 32
    softs    = []

    def del_soft(self, conf, soft, hbox, vbox):
        confirm = ConfirmDialog(
            self,
            _('Confirmation of deletion'),
            _('Do you really want to delete this app from Fluxbox launch ?')
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
            start_stream.append('exec %s &\n' % s.cmd)
            new_toml = dict(
                new_toml, 
                **s.to_dict(inc)
            )
        update_startup_file(conf.start_path, start_stream)
        with open(conf.toml_path,'w') as f:
            f.write(toml.dumps(new_toml))
        vbox.remove(hbox)

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
            os.path.isfile(soft.icon)
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
        else:
            img.set_from_icon_name(soft.icon, self.ICONSIZE)
            img.set_pixel_size(self.ICONSIZE)
        
        label = Gtk.Label(soft.name)

        hbox.pack_start(delbtn, True,  True, False)
        hbox.pack_start(img,    True,  True, False)
        hbox.pack_start(label,  True,  True, False)
        vbox.pack_end(hbox,     False, True, False)
        
        self.softs.append(soft)

    def on_drag_data_received(
        self, widget, context, x, y,
        selection, target_type, timestamp,
        conf, vbox
    ):

        data = selection.get_data().strip().replace('%20', ' ')
        f = data.replace("file://", "").strip()
        if os.path.isfile(f):
            soft = Soft()
            soft.new(*get_info_desktop(f))
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
                start_stream.append('exec %s &\n' % s.cmd)
            update_startup_file(conf.start_path, start_stream)
            with open(conf.toml_path, 'a+') as f:
                f.write(
                    ' \n'
                    + toml.dumps(soft.to_dict(len(self.softs)))
                )

    def appfinder(self, widget=None, event=None):
        os.system('rox /usr/share/applications &')

    def load(self, conf, vbox):
        start_stream  = []
        self.cmd_list = []
        new_toml      = {}
        if not os.path.isfile(conf.toml_path):
            return start_stream, new_toml
        with open(conf.toml_path,'r') as d:
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
        for soft_index in parsed_toml:
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
            self._add_soft(conf, soft, vbox)
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
        l = Gtk.Label(_(
            "Drag an application here to create a launcher"
        ))
        drag_vbox = Gtk.VBox(homogeneous=False)
        appfinderbtn = Gtk.Button(
            label = _("Search an application")
        )
        appfinderbtn.connect("button_press_event", self.appfinder)
        drag_vbox.pack_start(appfinderbtn, False, False, 10)
        drag_vbox.pack_start(l, True, True, 10)
        appfinderbtn.show()
        l.show()
        h.pack_start(drag_vbox, True, True, False)
        vbox.pack_start(h, True, True, False)

        start_stream, new_toml = self.load(conf, vbox)
        update_startup_file(conf.start_path, start_stream)
        with open(conf.toml_path,'w') as f:
            f.write(toml.dumps(new_toml))

        swin = Gtk.ScrolledWindow()
        swin.add_with_viewport(vbox)
        self.add(swin)
        self.set_default_size(400, 600)
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
