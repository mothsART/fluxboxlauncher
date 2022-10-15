import os

from gi.repository import Gtk
from gi.repository.GdkPixbuf import Pixbuf, InterpType


def new_img(icon, force_icon_size = None):
    icon_size = 48
    if force_icon_size:
        icon_size = force_icon_size
    image = Gtk.Image()
    if icon.endswith(('.png', '.jpg', '.ico', '.svg')) and os.path.isfile(icon):
            pixbuf = Pixbuf.new_from_file(icon)
            scaled_buf = pixbuf.scale_simple(
                icon_size,
                icon_size,
                InterpType.BILINEAR
            )
            image.set_from_pixbuf(scaled_buf)
    else:
        image.set_from_icon_name(icon, Gtk.IconSize.BUTTON)
        image.set_pixel_size(icon_size)
        icon_theme = Gtk.IconTheme.get_default()
        icon_info = icon_theme.lookup_icon(
            icon,
            Gtk.IconSize.BUTTON,
            0
        )
        if not icon_info:
            return None
    return image
