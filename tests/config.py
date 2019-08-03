from unittest import TestCase
from lib.config import Conf


class TestConf(TestCase):
    def test_load(self):
        conf = Conf('primtux')
        conf.load([], '', '')
    
    def test_add(self):
        conf = Conf('primtux')
        conf.load([], '', '')
        
