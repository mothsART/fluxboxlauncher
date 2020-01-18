{ lib
, python3
, gtk3
, gobject-introspection
, gettext
, buildPythonApplication ? python3.pkgs.buildPythonApplication
}:

buildPythonApplication rec {
  pname = "fluxboxlauncher";
  version = "0.1";

  src = lib.cleanSource ./.;

  buildInputs = [
    gobject-introspection
    gtk3
  ];

  propagatedBuildInputs = with python3.pkgs; [
    pygobject3
  ];

  meta = with lib; {
    description = "Fluxboxlauncher";
    homepage = "https://github.com/mothsART/fluxboxlauncher";
    maintainers = with maintainers; [ mothsart ];
    license = licenses.bsdOriginal;
    platforms = platforms.unix;
  };
}
