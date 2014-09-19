import datetime

from django.utils import timezone
#from django.test import TestCase
#from django.test import SimpleTestCase

from .utils import get_filebrowser_vo
from django.conf import settings

#class FileBrowserTests(SimpleTestCase):
#
#    def test_settings_vo(self):
#        """
#            test_settings_vo
#        """
#        vo = get_filebrowser_vo()
#        self.assertEqual(vo, getattr(settings, "FILEBROWSER_VO", "atlas"))


from django.utils import unittest
from django.test.client import Client



class SimpleFileBrowserTest(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_settings_vo(self):
        """
            test_settings_vo
        """
        vo = get_filebrowser_vo()
        self.assertEqual(vo, getattr(settings, "FILEBROWSER_VO", "atlas"))

