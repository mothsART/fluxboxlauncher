from gi.repository import Gtk, Gdk

def gtk_style():
    css = b"""
.icon {
    padding: 5px;
}

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
