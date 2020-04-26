import gettext
import sys
from os.path import dirname, join

from .debug import is_debug_mode

if is_debug_mode():
    LOCAL_PATH = join(dirname(dirname(__file__)), 'locale')
else:
    d = dirname(sys.modules['flxl'].__file__)
    LOCAL_PATH = join(d, '..', '..', '..', '..', 'share', 'locale')

gettext.bindtextdomain('fluxboxlauncher', LOCAL_PATH)
gettext.textdomain('fluxboxlauncher')
_ = gettext.gettext

_duplicate = _('Duplicate')
_app_already_exists = _('This application already exists')

_confirmation = _('Confirmation of deletion')
_confirm_question = _(
    'Do you really want to delete this app from Fluxbox launch ?'
)

_drag = _('Drag an application here to create a launcher')
_search = _('Search an application')

_activate = _('activate ?')

_add_cmd_line = _('Add command line')
