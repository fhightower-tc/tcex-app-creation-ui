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
    return render_template("index.html")


@app.route("/app-details")
def get_app_details():
    if request.args.get('appName'):
        return render_template("app-details.html", app_name=request.args['appName'])
    else:
        flash('Please enter a name for this app.', 'error')
        return redirect(url_for('index'))


def prepare_install_json(request):
    """Prepare the install.json with the correct parameters and output variables."""
    with open(os.path.abspath(os.path.join(os.path.dirname(__file__), "./templates/install.json.template"))) as f:
        install_json_template = f.read()

    install_json = json.loads(install_json_template % (request.args['parameters'], request.args['outputVariables'], request.args['appName']))
    return json.dumps(install_json, indent=4)


def prepare_tcex_app(request):
    """Prepare the python app with the correct parameters and output variables."""
    app_template = None

    with open(os.path.abspath(os.path.join(os.path.dirname(__file__), "./templates/playbook_app.template"))) as f:
        app_template = f.read()

    # handle input variables
    parameters = json.loads(request.args['parameters'])
    parameters_string = str()

    for parameter in parameters:
        if not parameter.get('required'):
            parameter['required'] = False
        parameters_string += "tcex.parser.add_argument('--{}', help='{}', required={})".format(parameter['name'], parameter['label'], parameter['required'])

    # handle output variables
    output_variables = json.loads(request.args['outputVariables'])
    outputVariableString = str()

    for variable in output_variables:
        outputVariableString += "tcex.playbook.create_output('{}', TODO: add a value here)".format(variable['name']) + "\n"

    app_template = app_template.format(outputVariableString, parameters_string)

    return app_template


@app.route("/tcex")
def tcex():
    if request.args.get('appName') and request.args.get('parameters') and request.args.get('outputVariables'):
        install_json = prepare_install_json(request).replace('\n', '<br>').replace(' ', '&nbsp;')
        app = prepare_tcex_app(request)

        return render_template('tcex.html', install_json=install_json, app=app, app_name=request.args['appName'])
    else:
        flash('Please enter a name for this app.', 'error')
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
