{ lib
, python3
, gtk3
, wrapGAppsHook
, glibcLocales
, gobject-introspection
, gettext
, pango
, gdk-pixbuf
, atk
}:

python3.pkgs.buildPythonApplication rec {
  pname = "fluxboxlauncher";
  version = "0.1";

  src = lib.cleanSource ./.;

  nativeBuildInputs = [
    wrapGAppsHook
    gobject-introspection
    pango
    gdk-pixbuf
    atk
    gettext
    glibcLocales
  ];

  buildInputs = [
    gtk3
    python3
  ];

  makeWrapperArgs = [ "--set LOCALE_ARCHIVE ${glibcLocales}/lib/locale/locale-archive"
                      "--set CHARSET en_us.UTF-8" ];

  propagatedBuildInputs = with python3.pkgs; [
    pygobject3
  ];

  meta = with lib; {
    description = "Fluxboxlauncher";
    homepage = "https://github.com/mothsART/fluxboxlauncher";
    maintainers = with maintainers; [ "mothsart" ];
    license = licenses.bsdOriginal;
    platforms = platforms.unix;
  };
}
