# -*- coding: utf-8 -*-
from collective.js.cycle2.config import PROJECTNAME
from collective.js.cycle2.controlpanel import ICycle2Settings
from collective.js.cycle2.testing import INTEGRATION_TESTING
from plone import api
from plone.app.testing import logout
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

import unittest


class ControlPanelTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.controlpanel = self.portal['portal_controlpanel']

    def test_controlpanel_has_view(self):
        request = self.layer['request']
        view = api.content.get_view(u'cycle2-settings', self.portal, request)
        view = view.__of__(self.portal)
        self.assertTrue(view())

    def test_controlpanel_view_is_protected(self):
        from AccessControl import Unauthorized
        logout()
        with self.assertRaises(Unauthorized):
            self.portal.restrictedTraverse('@@cycle2-settings')

    def test_controlpanel_installed(self):
        actions = [a.getAction(self)['id']
                   for a in self.controlpanel.listActions()]
        self.assertIn('cycle2', actions, 'control panel not installed')

    def test_controlpanel_removed_on_uninstall(self):
        qi = self.portal['portal_quickinstaller']

        with api.env.adopt_roles(['Manager']):
            qi.uninstallProducts(products=[PROJECTNAME])

        actions = [a.getAction(self)['id']
                   for a in self.controlpanel.listActions()]
        self.assertNotIn('cycle2', actions, 'control panel not removed')


class RegistryTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.registry = getUtility(IRegistry)
        self.settings = self.registry.forInterface(ICycle2Settings)

    def test_paused_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'paused'))
        self.assertEqual(self.settings.paused, True)

    def test_allow_wrap_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'allow_wrap'))
        self.assertEqual(self.settings.allow_wrap, True)

    def test_caption_template_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'caption_template'))
        self.assertEqual(self.settings.caption_template, u'{{slideNum}} / {{slideCount}}')

    def test_pager_template_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'pager_template'))
        self.assertEqual(self.settings.pager_template, u'<span>&bull;</span>')

    def test_speed_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'speed'))
        self.assertEqual(self.settings.speed, 500)

    def test_timeout_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'timeout'))
        self.assertEqual(self.settings.timeout, 4000)

    def test_transition_effect_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'transition_effect'))
        self.assertEqual(self.settings.transition_effect, 'fade')

    def test_default_image_size_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'default_image_size'))
        self.assertEqual(self.settings.default_image_size, 'preview')

    def test_records_removed_on_uninstall(self):
        qi = self.portal['portal_quickinstaller']

        with api.env.adopt_roles(['Manager']):
            qi.uninstallProducts(products=[PROJECTNAME])

        records = [
            ICycle2Settings.__identifier__ + '.paused',
            ICycle2Settings.__identifier__ + '.allow_wrap',
            ICycle2Settings.__identifier__ + '.caption_template',
            ICycle2Settings.__identifier__ + '.pager_template',
            ICycle2Settings.__identifier__ + '.speed',
            ICycle2Settings.__identifier__ + '.timeout',
            ICycle2Settings.__identifier__ + '.transition_effect',
            ICycle2Settings.__identifier__ + '.default_image_size',
        ]

        for r in records:
            self.assertNotIn(r, self.registry)
