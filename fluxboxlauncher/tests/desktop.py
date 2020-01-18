from unittest import TestCase
from unittest.mock import patch, mock_open

from fluxboxlauncher.lib.desktop import get_info

desktop_stream = """"[Desktop Entry]
Version=1.0
Name=MagicolorGrid
Comment=Create a magic color grid
Exec=magicolorgrid
Icon=/usr/share/applications/magicolorgrid/favicon.png
Terminal=false
Type=Application
Categories=Graphics;Illustration;
Keywords=svg;interactive;education;
Name[fr_FR]=magicolorgrid.desktop
"""


class TestDesktop(TestCase):

    @patch('builtins.open', mock_open(read_data=desktop_stream))
    def test_info(self):
        name, cmd, icon, generic = get_info('magicolorgrid.desktop')
        assert name == 'MagicolorGrid'
        assert cmd == 'magicolorgrid'
        assert icon == '/usr/share/applications/magicolorgrid/favicon'
        assert generic == ''
