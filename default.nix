{
    lib,
    python3,
    gtk3,
    gobject-introspection,
    buildPythonApplication ? python3.pkgs.buildPythonApplication
}:

buildPythonApplication rec {
    pname = "fluxboxlauncher";
    version = "0.1";

    src = ./.;

    nativeBuildInputs = [
        gobject-introspection
    ];

    buildInputs = [
        gtk3
    ];

    meta = with lib; {
        description = "Fluxboxlauncher";
        homepage = "https://github.com/mothsART/fluxboxlauncher";
        maintainers = with maintainers; [ mothsart ];
        license = licenses.bsdOriginal;
        platforms = platforms.unix;
    };
}
