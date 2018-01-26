#!/usr/bin/env python
# -*- coding: utf-8 -*-

import html
import unittest

from flask import url_for

from playbook_app_creator import playbook_app_creator


def _test_heading(response):
    """Make sure the heading is correct."""
    assert 'Playbook App Creator' in response
    assert 'App to aid the creation of playbook apps for ThreatConnect.' in response


def _test_code_block(response):
    """Make sure there is a code block in the response."""
    strings = ['def main():', 'if __name__ == &#34;__main__&#34;:', 'from tcex import TcEx', '# -*- coding: utf-8 -*-']

    for string in strings:
        try:
            assert string in response
        except AssertionError:
            raise AssertionError("Unable to find {} in {}".format(string, response))


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
        _test_code_block(rv.data.decode())
        assert 'tcex.playbook.create_output(output1, TODO: add a value here)' in rv.data.decode()


class PlaybookAppCreatorIncorrectRequestsTestCase(unittest.TestCase):

    def setUp(self):
        self.app = playbook_app_creator.app.test_client()

    def test_get_inputs_without_arguments(self):
        """This should redirect back to the index."""
        rv = self.app.get('/app-details', follow_redirects=True)
        _test_heading(rv.data.decode())

    def test_tcex_without_arguments(self):
        """This should redirect to the index."""
        rv = self.app.get('/tcex', follow_redirects=True)
        _test_heading(rv.data.decode())
