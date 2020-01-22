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

  propagatedBuildInputs = with python3.pkgs; [
    pygobject3
  ];

    postPatch = ''
    substituteInPlace flxl/lib/i18n.py \
      --replace "/usr" "$out"
  '';

  meta = with lib; {
    description = "Fluxboxlauncher";
    homepage = "https://github.com/mothsART/fluxboxlauncher";
    maintainers = with maintainers; [ mothsart ];
    license = licenses.bsdOriginal;
    platforms = platforms.unix;
  };
}
