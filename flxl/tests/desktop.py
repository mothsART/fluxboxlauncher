from unittest import TestCase
from unittest.mock import mock_open, patch

from flxl.lib.desktop import get_info

desktop_stream = """"[Desktop Entry]
Version=1.0
Name=MagicolorGrid
Comment=Create a magic color grid
Exec=magicolorgrid
Icon=/usr/share/applications/123/favicon.png
Terminal=false
Type=Application
Categories=Graphics;Illustration;
Keywords=svg;interactive;education;
Name[fr_FR]=MagicolorGrid en français
"""


class TestDesktop(TestCase):

    @patch('builtins.open', mock_open(read_data=desktop_stream))
    def test_info(self):
        name, cmd, icon, generic = get_info('magicolorgrid.desktop', 'fr_FR')
        assert name == 'MagicolorGrid en français'
        assert cmd == 'magicolorgrid'
        assert icon.startswith('/usr/share/applications/123/favicon')
        assert generic == ''
