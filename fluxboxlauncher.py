import os
import sys
import pygtk
pygtk.require('2.0')
import gtk
import gettext
import locale
import toml

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


class Conf:
    def __init__(self, user):
        self.DEBUG = False
        self.toml_path = 'start.toml'
        self.start_path = 'start_example'
        if os.path.isdir('.git'):
            self.DEBUG = True
        dirname = "/home/%s/.fluxbox/" % user
        if not os.path.isdir(dirname):
            return
        self.toml_path  = dirname + 'start.toml'
        self.start_path = dirname + 'start'


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


class FluxBoxLauncher:
    ICONSIZE = 32
    softs    = []

    def close_application(self, widget, event):
        gtk.main_quit()

    def del_soft(self, conf, soft, hbox, vbox):
        print(conf, soft, hbox, vbox)
        
        self.softs.remove(soft)
        new_toml = {}
        inc = 0
        start_stream = ''
        for s in self.softs:
            inc = inc + 1
            start_stream += 'exec %s &\n' % s.cmd
            new_toml = dict(
                new_toml, 
                **s.to_dict(inc)
            )
        with open(conf.toml_path,'w') as f:
            f.write(toml.dumps(new_toml))
        with open(conf.start_path,'w') as f:
            f.write(start_stream)
        vbox.remove(hbox)

    def _add_soft(self, conf, soft, vbox):
        hbox = gtk.HBox(homogeneous=False)

        delbtn = gtk.Button()
        deli = gtk.Image()
        deli.set_from_stock(gtk.STOCK_DELETE, gtk.ICON_SIZE_MENU)
        delbtn.set_image(deli)
        delbtn.connect_object(
            "clicked",
            self.del_soft,
            conf,
            soft,
            hbox,
            vbox
        )

        img = gtk.Image()
        if (
            os.path.isfile(soft.icon)
            and (icon.endswith('.png') or icon.endswith('.jpg'))
        ):
            pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(
                soft.icon,
                self.ICONSIZE, self.ICONSIZE
            )
            scaled_buf = pixbuf.scale_simple(
                self.ICONSIZE, self.ICONSIZE,
                gtk.gdk.INTERP_BILINEAR
            )
            img.set_from_pixbuf(scaled_buf)
        else:
            img.set_from_icon_name(soft.icon, self.ICONSIZE)
            img.set_pixel_size(self.ICONSIZE)
        
        label = gtk.Label(soft.name)

        hbox.pack_start(delbtn, True,  True)
        hbox.pack_start(img,    True,  True)
        hbox.pack_start(label,  True,  True)
        vbox.pack_end(hbox,     False, True)
        
        self.softs.append(soft)

    def on_drag_data_received(
        self, widget, context, x, y,
        selection, target_type, timestamp,
        conf, vbox
    ):
        data = selection.data.strip().replace('%20', ' ')
        f = data.replace("file://", "").strip()
        if os.path.isfile(f):
            soft = Soft()
            soft.new(*get_info_desktop(f))
            self._add_soft(conf, soft, vbox)
            vbox.show_all()
            with open(conf.toml_path, 'a+') as f:
                f.write(
                    ' \n'
                    + toml.dumps(soft.to_dict(len(self.softs)))
                )
            with open(conf.start_path,'a+') as f:
                f.write('exec %s &\n' % soft.cmd)

    def appfinder(self, widget=None, event=None):
        os.system('rox /usr/share/applications &')

    def load(self, conf, vbox):
        start_stream  = ''
        self.cmd_list = []
        new_toml      = {}
        if not os.path.isfile(conf.toml_path):
            return start_stream, new_toml
        with open(conf.toml_path,'r') as d:
            try:
                parsed_toml = toml.loads(d.read())
            except:
                print('start.toml is not a proper TOML file.')
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
            start_stream += 'exec %s &\n' % soft.cmd
            new_toml = dict(
                new_toml, 
                **soft.to_dict(len(self.softs))
            )
        return start_stream, new_toml

    def __init__(self, conf):
        if conf.DEBUG:
            print('DEBUG MODE')
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("delete_event", self.close_application)
        self.window.set_title("Fluxbox Launcher")
        self.window.set_border_width(0)

        vbox = gtk.VBox(homogeneous=False)
        
        TARGET_TYPE_URI_LIST = 80
        dnd_list = [ ( 'text/uri-list', 0, TARGET_TYPE_URI_LIST ) ]
        h = gtk.HBox(homogeneous=False)
        h.drag_dest_set(
            gtk.DEST_DEFAULT_MOTION |
            gtk.DEST_DEFAULT_HIGHLIGHT | gtk.DEST_DEFAULT_DROP,
            dnd_list, gtk.gdk.ACTION_COPY
        )
        h.connect(
            "drag_data_received",
            self.on_drag_data_received,
            conf, vbox
        )
        l = gtk.Label("Drag an icon here to create a launcher")
        drag_vbox = gtk.VBox(homogeneous=False)
        appfinderbtn = gtk.Button(label="Search for applications")
        appfinderbtn.connect("button_press_event", self.appfinder)
        drag_vbox.pack_start(appfinderbtn, False, False, 10)
        drag_vbox.pack_start(l, True, True, 10)
        appfinderbtn.show()
        l.show()
        h.pack_start(drag_vbox, True, True)
        vbox.pack_start(h, True, True)

        start_stream, new_toml = self.load(conf, vbox)
        with open(conf.start_path,'w') as f:
            f.write(start_stream)
        with open(conf.toml_path,'w') as f:
            f.write(toml.dumps(new_toml))

        swin = gtk.ScrolledWindow()
        swin.add_with_viewport(vbox)
        self.window.add(swin)
        self.window.set_default_size(400, 600)
        self.window.show_all()

if __name__ == "__main__":
    user = None
    if len(sys.argv) > 1:
        user = sys.argv[1]
    FluxBoxLauncher(Conf(user))
    gtk.main()
    exit(0)
