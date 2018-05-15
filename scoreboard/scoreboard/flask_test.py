#!/usr/bin/env python

from flask import Flask
from flask import request
from flask import render_template
from flask import redirect, url_for

import os


app = Flask(__name__)

@app.route('/')
def index():
    return "Home"
    # return render_template('index.html')


@app.route('/baseball', methods=['POST'])
def displayBaseball():
    os.system("sudo ./baseball.py")
    return "Baseball Displayed"
    # return redirect(url_for('index'))


@app.route('/quit')
def quit():
    func = request.environ.get('werkzeug.server.shutdown')
    func()
    return "Quitting..."


if __name__ == '__main__':
    # app.debug = True
    app.run(host='0.0.0.0')