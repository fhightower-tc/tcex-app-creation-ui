#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import shutil

from flask import flash, Flask, render_template, redirect, request, url_for
from cookiecutter.main import cookiecutter
from cookiecutter.exceptions import OutputDirExistsException


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
        app_name = request.args['appName'].replace(" ", "_").replace("-", "_")
        return render_template("app-details.html", app_name=app_name)
    else:
        flash('Please enter a name for this app.', 'error')
        return redirect(url_for('index'))


def prepare_install_json(request):
    """Prepare the install.json with the correct parameters and output variables."""
    with open(os.path.abspath(os.path.join(os.path.dirname(__file__), "./templates/install.json.template"))) as f:
        install_json_template = f.read()
    install_json = json.loads(install_json_template % (request.args['parameters'], request.args['outputVariables'], request.args['appName']))
    return json.dumps(install_json, indent=4)


# def prepare_tcex_app(request):
#     """Prepare the python app with the correct parameters and output variables."""
#     app_template = None

#     with open(os.path.abspath(os.path.join(os.path.dirname(__file__), "./templates/playbook_app.template"))) as f:
#         app_template = f.read()

#     # handle input variables
#     parameters = json.loads(request.args['parameters'])
#     parameters_string = str()

#     for parameter in parameters:
#         if not parameter.get('required'):
#             parameter['required'] = False
#         parameters_string += "tcex.parser.add_argument('--{}', help='{}', required={})".format(parameter['name'], parameter['label'], parameter['required'])

#     # handle output variables
#     output_variables = json.loads(request.args['outputVariables'])
#     outputVariableString = str()

#     for variable in output_variables:
#         outputVariableString += "tcex.playbook.create_output('{}', TODO: add a value here)".format(variable['name']) + "\n"

#     app_template = app_template.format(outputVariableString, parameters_string)

#     return app_template


def package_app(app_name):
    """Create a tcex app."""
    context_data = {
        'author_name': '',
        'project_name': app_name,
        'project_slug': app_name,
        'project_description': '',
        'version': '0.1.0',
        'runtime_level': 'Playbook',
        'open_source_license': 'Not open source'
    }

    try:
        cookiecutter('https://github.com/fhightower-templates/tcex-app-template.git', no_input=True, extra_context=context_data, output_dir=os.path.abspath(os.path.join(os.path.dirname(__file__), "./static/apps/")))
    except OutputDirExistsException:
        # TODO: there may be a better way to handle an existing directory (we may want to warn the user or force them to use a different name), but this will suffice for now
        existing_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "./static/apps/{}".format(app_name)))
        shutil.rmtree(existing_dir, ignore_errors=True)
        package_app(app_name)


def update_app(app_name, parameters, output_variables, python_file):
    """Update the install.json and the python app."""
    # replace the install.json with the updated version
    install_json_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "./static/apps/{}/{}/install.json".format(app_name, app_name)))
    with open(install_json_file_path, 'r') as f:
        install_json = json.load(f)
    install_json['params'] = json.loads(parameters)
    install_json['playbook']['outputVariables'] = json.loads(output_variables)
    with open(install_json_file_path, 'w') as f:
        json.dump(install_json, f)

    # replace the python_file with the updated version
    python_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "./static/apps/{}/{}/{}.py".format(app_name, app_name, app_name)))
    with open(python_file_path, 'r') as f:
        python_file = f.read()

    # zip the new app
    top_level_app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "./static/apps/{}/".format(app_name)))
    shutil.make_archive(top_level_app_path, 'zip')


@app.route("/tcex")
def tcex():
    if request.args.get('appName') and request.args.get('parameters') and request.args.get('outputVariables'):
        install_json = prepare_install_json(request).replace('\n', '<br>').replace(' ', '&nbsp;')
        python_file = ''
        package_app(request.args['appName'])
        update_app(request.args['appName'], request.args['parameters'], request.args['outputVariables'], python_file)
        return render_template('tcex.html', install_json=install_json, python_file=python_file, app_name=request.args['appName'])
    else:
        flash('Please enter a name for this app.', 'error')
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
