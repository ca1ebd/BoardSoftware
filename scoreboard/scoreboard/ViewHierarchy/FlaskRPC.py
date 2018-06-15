#!/usr/bin/env python
import json
import rgbmatrix.core
from flask import Flask, request
import sys
import zipfile
import time
import subprocess
import os
from threading import Timer


from rgbViews import *
from baseballBoard import BaseballBoard
from soccerBoard import SoccerBoard
from lacrosseBoard import LacrosseBoard
from footballBoard import FootballBoard
from stopwatchBoard import StopwatchBoard
from bootBoard import BootBoard
from fake_board import FakeBoard


class FlaskRPC:

    def __init__(self):
        self.rootDir = '/home/pi/scoreboard/scoreboard/ViewHierarchy/'
        self.rootView = None
        self.board = None
        #self.createBoot()
        t = threading.Timer(0.5, self.startUpDelay)
        t.start()
        self.app = self.createApp()
        self.app.debug = True
        #self.app.run()
        self.app.run(host='0.0.0.0', port=80)

    def startUpDelay(self):
        subprocess.call("wget -qO- http://127.0.0.1/ &> /dev/null", shell=True)

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
                    print(data)
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
                return '{"Error":"Could not decode request json"}'

            # Get data from the request
            try:
                method = req['method']
                params = req['params']
                uid = req['id']
            except KeyError:
                return '{"Error":"Missing required entries in request json"}'

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

        # @app.route('/update/', methods=['POST'])
        # def update():
        #     try:
        #         f = request.files['update']
        #         dir = '/home/pi/scoreboard/update/'
        #         # newDir = os.path.dirname(dir)
        #         # os.makedirs(newDir)
        #         # os.system("mkdir " + dir)
        #         subprocess.call('mkdir ' + dir, shell=True)
        #         zipName = 'update.zip'
        #         f.save(dir + zipName)
        #         zipRef = zipfile.ZipFile(dir + zipName, 'r')
        #         zipRef.extractall(dir)
        #         zipRef.close()
        #         subprocess.call('')
        #         subprocess.call('cd /home/pi/scoreboard/update && sh /home/pi/scoreboard/update/update.sh > log.txt', shell=True)
        #         subprocess.call('rm -rf /home/pi/scoreboard/update', shell=True)
        #     except Exception:
        #         return '{"Status":"Fail"}'
        #     return '{"Status":"OK"}'

        @app.route('/quit/')
        def quit():
            request.environ.get('werkzeug.server.shutdown')()
            return "Quitting..."

        @app.before_first_request
        def before_first():
            self.createBoot()

        return app

    def start(self, dataStr=None):
        if self.rootView is None:
            self.rootView = RGBBase()
        else:
            self.rootView.removeAllViews()
        return 'Success'

    def createBaseball(self, dataStr=None):
        if self.rootView == None:
            self.start()
        self.clear()
        #self.board = BaseballBoard(self.rootView)
        self.board = FakeBoard(self.rootView)

    def createSoccer(self, dataStr=None):
        if self.rootView == None:
            self.start()
        self.clear()
        self.board = SoccerBoard(self.rootView)

    def createFootball(self, dataStr=None):
        if self.rootView == None:
            self.start()
        self.clear()
        self.board = FootballBoard(self.rootView)

    def createLacrosse(self, dataStr=None):
        if self.rootView == None:
            self.start()
        self.clear()
        self.board = LacrosseBoard(self.rootView)

    def createStopwatch(self, dataStr=None):
        if self.rootView == None:
            self.start()
        self.clear()
        self.board = StopwatchBoard(self.rootView)

    def createBoot(self, dataStr=None):
        if self.rootView == None:
            self.start()
        self.clear()
        self.board = BootBoard(self.rootView)

    def info(self, dataStr=None):
        return "Connected"

    def clear(self, dataStr=None):
        self.rootView.removeAllViews()


if __name__ == '__main__':
    web = FlaskRPC()
    # time.sleep(.5)
    # web.startUpDelay()
    # print("Ran")
    #web.createBoot("null")

