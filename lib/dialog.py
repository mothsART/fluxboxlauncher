import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


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
