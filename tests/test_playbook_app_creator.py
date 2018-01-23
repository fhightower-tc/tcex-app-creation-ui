#!/usr/bin/env python
# -*- coding: utf-8 -*-

import html
import unittest

from playbook_app_creator import playbook_app_creator


def _test_heading(response):
    """."""
    assert 'Playbook App Creator' in response
    assert 'App to aid the creation of playbook apps for ThreatConnect.' in response


class PlaybookAppCreatorTestCase(unittest.TestCase):

    def setUp(self):
        self.app = playbook_app_creator.app.test_client()

    def test_get_index(self):
        rv = self.app.get('/')
        _test_heading(rv.data.decode())

    def test_get_inputs(self):
        rv = self.app.get('/app-details?appName=test_app')
        _test_heading(rv.data.decode())
        self.assertIn('Input Parameters', rv.data.decode())
        self.assertIn('Logic', rv.data.decode())
        self.assertIn('Output Variables', rv.data.decode())

    def test_output_tcex(self):
        rv = self.app.get('/tcex?parameters=%5B%7B"validValues"%3A""%2C"required"%3Afalse%2C"playbookDataType"%3A""%2C"note"%3A""%2C"hidden"%3Afalse%2C"encrypt"%3Afalse%2C"default"%3Afalse%2C"allowMultiple"%3Afalse%2C"type"%3A"c"%2C"name"%3A"b"%2C"label"%3A"a"%7D%5D&outputVariables=%5B%7B"type"%3A"String"%2C"name"%3A"output1"%7D%5D&appName=test_app&submit=Submit')
        _test_heading(rv.data.decode())
        self.assertIn('install.json', rv.data.decode())
        self.assertIn('test_app.py', rv.data.decode())
        self.assertIn('"label":&nbsp;"a"', rv.data.decode())
        self.assertIn('"name":&nbsp;"b",', rv.data.decode())
        self.assertIn('"type":&nbsp;"c",', rv.data.decode())
