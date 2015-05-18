# -*- coding: utf-8 -*-
from collective.js.cycle2.interfaces import IAddOnInstalled
from collective.js.cycle2.testing import INTEGRATION_TESTING
from plone import api
from plone.browserlayer import utils
from zope.interface import Interface

import unittest


class UpgradeTestCaseBase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self, from_version, to_version):
        self.portal = self.layer['portal']
        self.setup = self.portal['portal_setup']
        self.profile_id = u'collective.js.cycle2:default'
        self.from_version = from_version
        self.to_version = to_version

    def _get_upgrade_step(self, title):
        """Get one of the upgrade steps.

        Keyword arguments:
        title -- the title used to register the upgrade step
        """
        self.setup.setLastVersionForProfile(self.profile_id, self.from_version)
        upgrades = self.setup.listUpgrades(self.profile_id)
        steps = [s for s in upgrades[0] if s['title'] == title]
        return steps[0] if steps else None

    def _do_upgrade_step(self, step):
        """Execute an upgrade step.

        Keyword arguments:
        step -- the step we want to run
        """
        request = self.layer['request']
        request.form['profile_id'] = self.profile_id
        request.form['upgrades'] = [step['id']]
        self.setup.manage_doUpgrades(request=request)

    def _how_many_upgrades_to_do(self):
        self.setup.setLastVersionForProfile(self.profile_id, self.from_version)
        upgrades = self.setup.listUpgrades(self.profile_id)
        assert len(upgrades) > 0
        return len(upgrades[0])


class Upgrade1000to1001TestCase(UpgradeTestCaseBase):

    def setUp(self):
        UpgradeTestCaseBase.setUp(self, u'1000', u'1001')

    def test_upgrade_to_1001_registrations(self):
        version = self.setup.getLastVersionForProfile(self.profile_id)[0]
        self.assertGreaterEqual(int(version), int(self.to_version))
        self.assertEqual(self._how_many_upgrades_to_do(), 1)

    def test_issue_1(self):
        # check if the upgrade step is registered
        title = u'Remove browser layer and jsregistry'
        description = u'We don\'t need a profile for this package.'
        step = self._get_upgrade_step(title)
        self.assertIsNotNone(step)
        self.assertEqual(step['description'], description)

        js_tool = self.portal['portal_javascripts']
        JS_IDS = [
            '++resource++collective.js.cycle2/jquery.cycle2.min.js',
            '++resource++collective.js.cycle2/jquery.cycle2.center.min.js',
            '++resource++collective.js.cycle2/jquery.cycle2.swipe.min.js'
        ]
        for js_id in JS_IDS:
            js_tool.registerResource(js_id)

        resource_ids = js_tool.getResourceIds()
        for js_id in JS_IDS:
            self.assertIn(js_id, resource_ids)

        utils.register_layer(IAddOnInstalled, name='collective.js.cycle2')
        self.assertIn(IAddOnInstalled, utils.registered_layers())

        self._do_upgrade_step(step)

        resource_ids = js_tool.getResourceIds()
        for js_id in JS_IDS:
            self.assertNotIn(js_id, resource_ids)

        self.assertNotIn(IAddOnInstalled, utils.registered_layers())
