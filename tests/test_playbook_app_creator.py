#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from playbook_app_creator import playbook_app_creator


class PlaybookAppCreatorTestCase(unittest.TestCase):

    def setUp(self):
        self.app = playbook_app_creator.app.test_client()

    def test_get_index(self):
        rv = self.app.get('/')
        self.assertIn('Playbook App Creator', rv.data.decode())
        self.assertIn('App to aid the creation of playbook apps for ThreatConnect.', rv.data.decode())
