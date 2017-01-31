# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from medialog.dgh.testing import MEDIALOG_DGH_INTEGRATION_TESTING  # noqa

import unittest


class TestSetup(unittest.TestCase):
    """Test that medialog.dgh is properly installed."""

    layer = MEDIALOG_DGH_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if medialog.dgh is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'medialog.dgh'))

    def test_browserlayer(self):
        """Test that IMedialogDghLayer is registered."""
        from medialog.dgh.interfaces import (
            IMedialogDghLayer)
        from plone.browserlayer import utils
        self.assertIn(IMedialogDghLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = MEDIALOG_DGH_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['medialog.dgh'])

    def test_product_uninstalled(self):
        """Test if medialog.dgh is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'medialog.dgh'))

    def test_browserlayer_removed(self):
        """Test that IMedialogDghLayer is removed."""
        from medialog.dgh.interfaces import \
            IMedialogDghLayer
        from plone.browserlayer import utils
        self.assertNotIn(IMedialogDghLayer, utils.registered_layers())
