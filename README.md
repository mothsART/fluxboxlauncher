<div align="center">
    <img src="./ressources/logo.svg" alt="Fluxboxlauncher logo" width="100"/>
    <h1>FluxboxLauncher</h1>
    <p>
        <a href="https://travis-ci.org/mothsART/fluxboxlauncher" rel="nofollow">
            <img src="https://camo.githubusercontent.com/9c74f5bdefbed698c50cee9a07474ef105307713/68747470733a2f2f7472617669732d63692e6f72672f6d6f7468734152542f666c7578626f786c61756e636865722e706e673f6272616e63683d6d6173746572" alt="Build Status" data-canonical-src="https://travis-ci.org/mothsART/fluxboxlauncher.png?branch=master" style="max-width:100%;">
        </a>
        <a href="/mothsART/fluxboxlauncher/blob/master/LICENSE">
            <img src="https://camo.githubusercontent.com/6def34e1aa4e2e9e81448c8a57cf3e09d8af28cf/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f6c6963656e73652d4253442d626c75652e737667" alt="LICENSE" data-canonical-src="https://img.shields.io/badge/license-BSD-blue.svg" style="max-width:100%;">
        </a>
    </p>
</div>

## Introduction

Manage application startup when FluxBox is launched :
FluxBoxlauncher is a graphical application with drag-and-drop functionality.

### Last stable version

[![Packaging status](https://repology.org/badge/vertical-allrepos/fluxboxlauncher.svg)](https://repology.org/project/fluxboxlauncher/versions)

- Ubuntu 18.04, 19.10 and 20.04: [PPA](https://launchpad.net/~jerem-ferry/+archive/ubuntu/fluxbox)

## Dependances

python-gtk

## launch

```sh
./fluxboxlauncher.py USERNAME
```

## i18n

Create pot file :

```sh
pygettext -o fluxboxlauncher.pot ./fluxboxlauncher.py
```

Compile po file to mo :

```sh
msgfmt -o locale/{lang}/LC_MESSAGES/fluxboxlauncher.mo locale/{lang}/LC_MESSAGES/fluxboxlauncher.po
```

ie : in french

```sh
msgfmt -o locale/fr/LC_MESSAGES/fluxboxlauncher.mo locale/fr/LC_MESSAGES/fluxboxlauncher.po
```

## Tests

```sh
python3 -m unittest flxl/tests/tests.py
```

## Create a Debian package

```sh
git clone https://github.com/mothsART/fluxboxlauncher.git
cd fluxboxlauncher
dpkg-buildpackage -us -uc
```

and launch with :

```sh
sudo dpkg -i ../fluxboxlauncher_*_all.deb
```

## Create a Nix package

```sh
nix-build
```

install locally :

```sh
nix-env -if .
```

launch locally :

```sh
nix run -c fluxboxlauncher
```
