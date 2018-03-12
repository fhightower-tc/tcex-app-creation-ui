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
        app_name = request.args['appName'].lower().replace(" ", "_").replace("-", "_")
        return render_template("app-details.html", app_name=app_name)
    else:
        flash('Please enter a name for this app.', 'error')
        return redirect(url_for('index'))


def create_app_from_template(app_name):
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
        # TODO: do we also need to remove the .zip file?
        create_app_from_template(app_name)


def _update_install_json(install_json_dict, parameters, output_variables):
    install_json_dict['params'] = parameters
    install_json_dict['playbook']['outputVariables'] = output_variables
    return install_json_dict


def _update_python_file(python_file_text, parameters, output_variables, app_name):
    """Update the python file that will contain the code for the app."""
    # handle input variables
    parameters_string = str()

    for parameter in parameters:
        if not parameter.get('required'):
            parameter['required'] = False
        parameters_string += "tcex.parser.add_argument('--{}', help='{}', required={})".format(parameter['name'], parameter['label'], parameter['required'])

    # handle output variables
    output_variables_string = str()

    for variable in output_variables:
        output_variables_string += "tcex.playbook.create_output('{}', TODO: add a value here)".format(variable['name']) + "\n"

    python_file_text = python_file_text.replace("tcex.parser.add_argument('--string', help='Input string', required=True)", parameters_string)
    python_file_text = python_file_text.replace("# output the reversed string to downstream playbook apps\n    tcex.playbook.create_output('{}.reversed_string', string[::-1])".format(app_name), output_variables_string)

    return python_file_text


def _update_readme(readme_text, parameters, output_variables):
    # TODO: we may want to use the 'note' field for the parameter if it has one
    parameters_string = ['- `{}` *({})*: {}'.format(parameter['name'], parameter['type'], parameter['label']) for parameter in parameters]
    output_variables_string = ['- `{}` *({})*'.format(output_variable['name'], output_variable['type']) for output_variable in output_variables]

    readme_text = readme_text.replace('Todo: add input definitions', '\n'.join(parameters_string))
    readme_text = readme_text.replace('Todo: add output definitions', '\n'.join(output_variables_string))
    readme_text = readme_text.replace("This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and [Floyd Hightower's TCEX App Template](https://github.com/fhightower-templates/tcex-app-template).", "This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and [Floyd Hightower's TCEX App Creation UI](http://tcex.hightower.space).")

    return readme_text


def update_app(app_name, parameters, output_variables):
    """Update the files in the template with the parameters and output variables."""
    parameters = json.loads(parameters)
    output_variables = json.loads(output_variables)

    # update install.json
    install_json_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "./static/apps/{}/{}/install.json".format(app_name, app_name)))
    with open(install_json_file_path, 'r') as f:
        install_json = json.load(f)
    install_json = _update_install_json(install_json, parameters, output_variables)
    with open(install_json_file_path, 'w') as f:
        json.dump(install_json, f)

    # update the python file
    python_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "./static/apps/{}/{}/{}.py".format(app_name, app_name, app_name)))
    with open(python_file_path, 'r') as f:
        python_file = f.read()
    updated_python_file = _update_python_file(python_file, parameters, output_variables, app_name)
    with open(python_file_path, 'w') as f:
        f.write(updated_python_file)

    # update readme.md
    readme_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "./static/apps/{}/README.md".format(app_name)))
    with open(readme_file_path, 'r') as f:
        readme = f.read()
    updated_readme = _update_readme(readme, parameters, output_variables)
    with open(readme_file_path, 'w') as f:
        f.write(updated_readme)

    # zip the new app
    top_level_app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "./static/apps/{}/".format(app_name)))
    shutil.make_archive(top_level_app_path, 'zip', top_level_app_path)

    return json.dumps(install_json, indent=4), updated_python_file


@app.route("/tcex")
def tcex():
    if request.args.get('appName') and request.args.get('parameters') and request.args.get('outputVariables'):
        create_app_from_template(request.args['appName'])
        install_json, python_file = update_app(request.args['appName'], request.args['parameters'], request.args['outputVariables'])
        return render_template('tcex.html', install_json=install_json, python_file=python_file, app_name=request.args['appName'])
    else:
        flash('Please enter a name for this app.', 'error')
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
