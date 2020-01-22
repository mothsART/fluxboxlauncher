import gettext
from os.path import dirname, join, exists

local_path = join(dirname(dirname(__file__)), 'locale')
if not exists(local_path):
    local_path = '/usr/share/locale'

gettext.bindtextdomain('fluxboxlauncher', local_path)
gettext.textdomain('fluxboxlauncher')
_ = gettext.gettext

_duplicate = _('Duplicate')
_app_already_exists = _('This application already exists')

_confirmation = _('Confirmation of deletion')
_confirm_question = _('Do you really want to delete this app from Fluxbox launch ?')

_drag = _("Drag an application here to create a launcher")
_search = _("Search an application")

_activate = _("activate ?")

_add_cmd_line = _('Add command line')
