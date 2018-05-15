#!/usr/bin/env python
import json
import rgbmatrix.core
from flask import Flask, request
import sys

from baseballParam import BaseballBoard

class FlaskRPC:

    def __init__(self):
        self.board = None
        self.app = self.createApp()
        self.app.run(host='0.0.0.0', port=80)

    def createApp(self):
        app = Flask(__name__)

        @app.route('/', methods=['GET', 'POST'])
        def hello():
            data = ''
            if request.method == 'GET':
                data = request.args.get('r', '')
            elif request.method == 'POST':
                if 'r' in request.form:
                    data = request.form['r']
                else:
                    data = request.data

            # Convert bytes to string if appropriate
            try:
                data = data.decode('utf-8')
            except AttributeError:
                pass

            # Convert data to the json format
            try:
                req = json.loads(data)
            except ValueError:
                return '{"Error":"Could not decode request JSON"}'

            # Get data from the request
            try:
                method = req['method']
                params = req['params']
                uid = req['id']
            except KeyError:
                return '{"Error":"Missing required entries in request JSON"}'

            # Call the method
            try:
                # Call the class/obj method is there is a '.'
                if '.' in method:
                    comps = method.split('.')
                    resp = getattr(getattr(self, comps[0]), comps[1])(params)
                else:  # Call the local method
                    resp = getattr(self, method)(params)
            except KeyError:
                return '{"Error":"Could not find the requested method"}'

            return '{"id":"%s", "response":"%s"}' % (uid, resp)
        return app

    def createBaseball(self, dataStr=None):
        self.board = BaseballBoard()

    def createSoccer(self, dataStr=None):
        a = None
        #self.board = SoccerBoard()

    def createFootball(self, dataStr=None):
        a = None
        #self.board = FootballBoard()

    def createLacrosse(self, dataStr=None):
        a = None
        #self.board = LacrosseBoard()

    def killBoard(self, dataStr=None):
        self.board.killEvent.set()





if __name__ == '__main__':
    web = FlaskRPC()