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


def _test_app_description(response, app_description):
    """Make sure the app description is in the python file and the install.json."""
    assert app_description in response
    assert response.count(app_description) == 2


def _test_install_json(response, app_description):
    """Make sure there is a code block in the response."""
    strings = ['"type": "String",', '"name": "b",', '"label": "a"', '"type": "String",', '"name": "output1"', '"programMain": "test_app",']

    for string in strings:
        try:
            assert string in response
        except AssertionError:
            raise AssertionError("Unable to find {} in {}".format(string, response))

    assert '"runtimeLevel": "Playbook"' in response

    # check to make sure the install.json is pretty-printed
    assert '"programLanguage": "python",\n    "programMain"' in response
    _test_app_description(response, app_description)


def _test_python_file(response, app_description, required=False):
    """Make sure there is a code block in the response."""
    strings = ['# -*- coding: utf-8 -*-', 'from tcex import TcEx', 'def main():', 'if __name__ == &#34;__main__&#34;:', "tcex.parser.add_argument(&#39;--b&#39;, help=&#39;a&#39;, required={})".format(required), "tcex.playbook.create_output(&#39;output1&#39;, TODO: add a value here)"]

    for string in strings:
        try:
            assert string in response
        except AssertionError:
            raise AssertionError("Unable to find {} in {}".format(string, response))

    _test_app_description(response, app_description)


class PlaybookAppCreatorTestCase(unittest.TestCase):

    def setUp(self):
        self.app = playbook_app_creator.app.test_client()

    def test_get_index(self):
        rv = self.app.get('/')
        _test_heading(rv.data.decode())

    def test_get_inputs(self):
        rv = self.app.get('/app-details?appName=test_app&appDescription=Testing app.')
        _test_heading(rv.data.decode())
        self.assertIn('Input Parameters', rv.data.decode())
        self.assertIn('Logic', rv.data.decode())
        self.assertIn('Output Variables', rv.data.decode())

    def test_name_with_space(self):
        rv = self.app.get('/app-details?appName=test app&appDescription=Testing app.')
        self.assertIn('value="test_app"', rv.data.decode())

    def test_name_with_trailing_space(self):
        rv = self.app.get('/app-details?appName=test app &appDescription=Testing app.')
        self.assertIn('value="test_app"', rv.data.decode())

    def test_name_with_uppercase(self):
        rv = self.app.get('/app-details?appName=Test App&appDescription=Testing app.')
        self.assertIn('value="test_app"', rv.data.decode())

    def test_install_json_output(self):
        """Make sure the install.json created by the app is correct."""
        app_description = 'App for testing.'
        rv = self.app.post('/tcex?appName=test_app', data={
            'parameters': '[{"validValues":"","required":false,"playbookDataType":"String","note":"","hidden":false,"encrypt":false,"default":false,"allowMultiple":false,"type":"String","name":"b","label":"a"}]',
            'outputVariables': '[{"type":"String","name":"output1"}]',
            'appName': 'test_app',
            'description': app_description,
            'displayName': 'Test App',
            'jobsApp': 'None'
        })
        assert rv.status_code == 200
        _test_heading(rv.data.decode())
        self.assertIn('install.json', rv.data.decode())
        # validate that inputs are shown
        _test_install_json(rv.data.decode(), app_description)

    def test_python_file(self):
        """Make sure the app created by the app is correct."""
        app_description = 'App for testing.'
        rv = self.app.post('/tcex', data={
            'parameters': '[{"validValues":"","required":false,"playbookDataType":"String","note":"","hidden":false,"encrypt":false,"default":false,"allowMultiple":false,"type":"String","name":"b","label":"a"}]',
            'outputVariables': '[{"type":"String","name":"output1"}]',
            'appName': 'test_app',
            'description': app_description,
            'displayName': 'Test App',
            'jobsApp': 'None'
        })
        assert rv.status_code == 200
        _test_heading(rv.data.decode())
        self.assertIn('test_app.py', rv.data.decode())
        # validate that outputs are shown
        _test_python_file(rv.data.decode(), app_description)

    def test_app_output_with_required_parameter(self):
        """Make sure the app created by the app is correct."""
        app_description = 'App for testing.'
        rv = self.app.post('/tcex', data={
            'parameters': '[{"validValues":"","required":true,"playbookDataType":"String","note":"","hidden":false,"encrypt":false,"default":false,"allowMultiple":false,"type":"String","name":"b","label":"a"}]',
            'outputVariables': '[{"type":"String","name":"output1"}]',
            'appName': 'test_app',
            'description': app_description,
            'displayName': 'Test App',
            'jobsApp': 'None'
        })
        assert rv.status_code == 200
        _test_heading(rv.data.decode())
        self.assertIn('test_app.py', rv.data.decode())
        # validate that outputs are shown
        _test_python_file(rv.data.decode(), app_description, True)


class JobsAppCreationTestCases(unittest.TestCase):

    def setUp(self):
        self.app = playbook_app_creator.app.test_client()

    def test_jobs_app_creation(self):
        rv = self.app.post('/tcex', data={
            'parameters': '[{"validValues":"","required":true,"playbookDataType":"String","note":"","hidden":false,"encrypt":false,"default":false,"allowMultiple":false,"type":"String","name":"b","label":"a"}]',
            'outputVariables': '[{"type":"String","name":"output1"}]',
            'appName': 'test_app',
            'description': 'App for testing.',
            'displayName': 'Test App',
            'jobsApp': 'on'
        })
        assert rv.status_code == 200

    def test_jobs_app_install_json(self):
        rv = self.app.post('/tcex', data={
            'parameters': '[{"validValues":"","required":true,"playbookDataType":"String","note":"","hidden":false,"encrypt":false,"default":false,"allowMultiple":false,"type":"String","name":"b","label":"a"}]',
            'outputVariables': '[{"type":"String","name":"output1"}]',
            'appName': 'test_app',
            'description': 'App for testing.',
            'displayName': 'Test App',
            'jobsApp': 'on'
        })
        assert rv.status_code == 200
        assert '"playbook":' not in rv.data.decode()
        assert '"runtimeLevel": "Organization"' in rv.data.decode()

    def test_jobs_app_python_file(self):
        rv = self.app.post('/tcex', data={
            'parameters': '[{"validValues":"","required":true,"playbookDataType":"String","note":"","hidden":false,"encrypt":false,"default":false,"allowMultiple":false,"type":"String","name":"b","label":"a"}]',
            'outputVariables': '[{"type":"String","name":"output1"}]',
            'appName': 'test_app',
            'description': 'App for testing.',
            'displayName': 'Test App',
            'jobsApp': 'on'
        })
        assert rv.status_code == 200
        assert 'tcex.message_tc' in rv.data.decode()
        assert 'tcex.playbook' not in rv.data.decode()


class CreatedAppFilesTestCases(unittest.TestCase):

    def setUp(self):
        self.app = playbook_app_creator.app.test_client()

    def test_readme_credits(self):
        """Make sure the credits in the readme are correct."""
        rv = self.app.post('/tcex', data={
            'parameters': '[{"validValues":"","required":true,"playbookDataType":"String","note":"","hidden":false,"encrypt":false,"default":false,"allowMultiple":false,"type":"String","name":"b","label":"a"}]',
            'outputVariables': '[{"type":"String","name":"output1"}]',
            'appName': 'test_app',
            'description': 'App for testing.',
            'displayName': 'Test App',
            'jobsApp': 'None'
        })
        assert rv.status_code == 200
        with open(os.path.abspath(os.path.join(os.path.dirname(__file__), "../playbook_app_creator/static/apps/test_app/README.md")), 'r') as f:
            readme_text = f.read()
            assert "[Cookiecutter](https://github.com/audreyr/cookiecutter) and [Floyd Hightower's TCEX App Creation UI](http://tcex.hightower.space)" in readme_text


class PlaybookAppCreatorIncorrectRequestsTestCase(unittest.TestCase):

    def setUp(self):
        self.app = playbook_app_creator.app.test_client()

    def test_app_details_without_arguments(self):
        """This should redirect back to the index."""
        rv = self.app.get('/app-details', follow_redirects=True)
        _test_index(rv.data.decode())
        assert 'Please enter a name for this app.' in rv.data.decode()
        assert 'Please enter a description for this app.' in rv.data.decode()

    def test_app_details_missing_app_description(self):
        rv = self.app.get('/app-details?appName=Test App', follow_redirects=True)
        _test_index(rv.data.decode())
        assert 'Please enter a name for this app.' not in rv.data.decode()
        assert 'Please enter a description for this app.' in rv.data.decode()
        assert 'Test App' in rv.data.decode()

    def test_app_details_missing_app_name(self):
        rv = self.app.get('/app-details?appDescription=Testing', follow_redirects=True)
        _test_index(rv.data.decode())
        assert 'Please enter a name for this app.' in rv.data.decode()
        assert 'Please enter a description for this app.' not in rv.data.decode()
        assert 'Testing' in rv.data.decode()

    def test_tcex_without_arguments(self):
        """This should redirect to the index."""
        rv = self.app.post('/tcex', follow_redirects=True)
        _test_index(rv.data.decode())
        assert 'Please enter a name for this app.' in rv.data.decode()
