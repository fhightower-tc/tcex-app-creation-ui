#!/usr/bin/env python
# -*- coding: utf-8 -*-

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


@app.route("/test")
def test():
    return request.args['parameters']


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
