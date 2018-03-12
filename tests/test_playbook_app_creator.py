#!/usr/bin/env python
# -*- coding: utf-8 -*-

import html
import os
import unittest

from flask import url_for

from playbook_app_creator import playbook_app_creator


def _test_heading(response):
    """Make sure the heading is correct."""
    assert 'TCEX App Creation UI' in response
    assert 'Create a ThreatConnect Exchange App!' in response


def _test_index(response):
    """Make sure the index page is shown."""
    assert 'Create a TCEX app' in response
    _test_heading(response)


def _test_install_json(response):
    """Make sure there is a code block in the response."""
    strings = ['"type": "String",', '"name": "b",', '"label": "a"', '"type": "String",', '"name": "output1"', '"programMain": "test_app",']

    for string in strings:
        try:
            assert string in response
        except AssertionError:
            raise AssertionError("Unable to find {} in {}".format(string, response))

    # check to make sure the install.json is pretty-printed
    assert '"programLanguage": "python",\n    "programMain"' in response


def _test_app(response, required=False):
    """Make sure there is a code block in the response."""
    strings = ['# -*- coding: utf-8 -*-', 'from tcex import TcEx', 'def main():', 'if __name__ == &#34;__main__&#34;:', "tcex.parser.add_argument(&#39;--b&#39;, help=&#39;a&#39;, required={})".format(required), "tcex.playbook.create_output(&#39;output1&#39;, TODO: add a value here)"]

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

    def test_name_with_space(self):
        rv = self.app.get('/app-details?appName=test app')
        self.assertIn('value="test_app"', rv.data.decode())

    def test_name_with_uupercase(self):
        rv = self.app.get('/app-details?appName=Test App')
        self.assertIn('value="test_app"', rv.data.decode())

    def test_install_json_output(self):
        """Make sure the install.json created by the app is correct."""
        rv = self.app.get('/tcex?parameters=%5B%7B"validValues"%3A""%2C"required"%3Afalse%2C"playbookDataType"%3A"String"%2C"note"%3A""%2C"hidden"%3Afalse%2C"encrypt"%3Afalse%2C"default"%3Afalse%2C"allowMultiple"%3Afalse%2C"type"%3A"String"%2C"name"%3A"b"%2C"label"%3A"a"%7D%5D&outputVariables=%5B%7B"type"%3A"String"%2C"name"%3A"output1"%7D%5D&appName=test_app&submit=Submit')
        _test_heading(rv.data.decode())
        self.assertIn('install.json', rv.data.decode())
        # validate that inputs are shown
        _test_install_json(rv.data.decode())

    def test_app_output(self):
        """Make sure the app created by the app is correct."""
        rv = self.app.get('/tcex?parameters=%5B%7B"validValues"%3A""%2C"required"%3Afalse%2C"playbookDataType"%3A"String"%2C"note"%3A""%2C"hidden"%3Afalse%2C"encrypt"%3Afalse%2C"default"%3Afalse%2C"allowMultiple"%3Afalse%2C"type"%3A"String"%2C"name"%3A"b"%2C"label"%3A"a"%7D%5D&outputVariables=%5B%7B"type"%3A"String"%2C"name"%3A"output1"%7D%5D&appName=test_app&submit=Submit')
        _test_heading(rv.data.decode())
        self.assertIn('test_app.py', rv.data.decode())
        # validate that outputs are shown
        _test_app(rv.data.decode())

    def test_app_output_with_required_parameter(self):
        """Make sure the app created by the app is correct."""
        rv = self.app.get('/tcex?parameters=%5B%7B"validValues"%3A""%2C"required"%3Atrue%2C"playbookDataType"%3A"String"%2C"note"%3A""%2C"hidden"%3Afalse%2C"encrypt"%3Afalse%2C"default"%3Afalse%2C"allowMultiple"%3Afalse%2C"type"%3A"String"%2C"name"%3A"b"%2C"label"%3A"a"%7D%5D&outputVariables=%5B%7B"type"%3A"String"%2C"name"%3A"output1"%7D%5D&appName=test_app&submit=Submit')
        _test_heading(rv.data.decode())
        self.assertIn('test_app.py', rv.data.decode())
        # validate that outputs are shown
        _test_app(rv.data.decode(), True)


class CreatedAppFilesTestCases(unittest.TestCase):

    def setUp(self):
        self.app = playbook_app_creator.app.test_client()

    def test_readme_credits(self):
        """Make sure the credits in the readme are correct."""
        rv = self.app.get('/tcex?parameters=%5B%7B"validValues"%3A""%2C"required"%3Atrue%2C"playbookDataType"%3A"String"%2C"note"%3A""%2C"hidden"%3Afalse%2C"encrypt"%3Afalse%2C"default"%3Afalse%2C"allowMultiple"%3Afalse%2C"type"%3A"String"%2C"name"%3A"b"%2C"label"%3A"a"%7D%5D&outputVariables=%5B%7B"type"%3A"String"%2C"name"%3A"output1"%7D%5D&appName=test_app&submit=Submit')
        with open(os.path.abspath(os.path.join(os.path.dirname(__file__), "../playbook_app_creator/static/apps/test_app/README.md")), 'r') as f:
            readme_text = f.read()
            assert "[Cookiecutter](https://github.com/audreyr/cookiecutter) and [Floyd Hightower's TCEX App Creation UI](http://tcex.hightower.space)" in readme_text


class PlaybookAppCreatorIncorrectRequestsTestCase(unittest.TestCase):

    def setUp(self):
        self.app = playbook_app_creator.app.test_client()

    def test_get_inputs_without_arguments(self):
        """This should redirect back to the index."""
        rv = self.app.get('/app-details', follow_redirects=True)
        _test_index(rv.data.decode())
        assert 'Please enter a name for this app.' in rv.data.decode()

    def test_tcex_without_arguments(self):
        """This should redirect to the index."""
        rv = self.app.get('/tcex', follow_redirects=True)
        _test_index(rv.data.decode())
        assert 'Please enter a name for this app.' in rv.data.decode()
