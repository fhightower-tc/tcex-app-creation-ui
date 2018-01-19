#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os

from flask import flash, Flask, render_template, redirect, request, url_for


class CustomFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        block_start_string='(%',
        block_end_string='%)',
        variable_start_string='((',
        variable_end_string='))',
        comment_start_string='(#',
        comment_end_string='#)',
    ))


app = CustomFlask(__name__)
app.secret_key = 'abc'


@app.route("/")
def index():
    # request.form['text']
    return render_template("index.html")


def prepare_install_json():
    """Prepare the install.json with the correct parameters and output variables."""
    with open(os.path.abspath(os.path.join(os.path.dirname(__file__), "./templates/install.json.template"))) as f:
        install_json_template = f.read()

    install_json = json.loads(install_json_template % (request.args['parameters'], request.args['outputVariables']))
    return json.dumps(install_json, indent=4)


def prepare_tcex_app():
    """Prepare the python app with the correct parameters and output variables."""
    # TODO: create the app template here
    app = "app_template_here"
    return app


@app.route("/test")
def test():
    install_json = prepare_install_json().replace('\n', '<br>').replace(' ', '&nbsp;')
    app = prepare_tcex_app()

    return render_template('tcex.html', install_json=install_json, app=app)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
