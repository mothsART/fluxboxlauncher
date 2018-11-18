# FluxboxLauncher

## Dependances

python-gtk
python-toml

## launch

```sh
python ./fluxboxlauncher.py USERNAME
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
