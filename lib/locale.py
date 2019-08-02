import gettext
from os.path import dirname, join

local_path = join(dirname(dirname(__file__)), 'locale')
gettext.bindtextdomain('fluxboxlauncher', local_path)
gettext.textdomain('fluxboxlauncher')
_ = gettext.gettext

_confirmation = _('Confirmation of deletion')
_confirm_question = _('Do you really want to delete this app from Fluxbox launch ?')

_drag = _("Drag an application here to create a launcher")
_search = _("Search an application")
