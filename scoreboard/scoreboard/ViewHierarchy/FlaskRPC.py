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
import traceback

from rgbViews import *
from baseballBoard import BaseballBoard
from soccerBoard import SoccerBoard
from lacrosseBoard import LacrosseBoard
from footballBoard import FootballBoard
from stopwatchBoard import StopwatchBoard
from bootBoard import BootBoard
from fake_board import FakeBoard

from RPCObjects import *

debug = True


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
            if request.args.has_key("r"):
                data = request.args["r"]
                if debug: print "Found JSON RPC Request in GET Variables!"
            elif request.form.get("r"):
                data = request.form["r"]
                if debug: print "Found JSON RPC Request in FORM Variables!"
            else:
                data = request.data
                if debug: print "Found JSON RPC Request in POST Data!"
            try:
                if debug: print data
                # Parse the request
                req = JsonRpcRequest(data)
                if debug: print req.__dict__
                # Handle the request

                # Provide a starting scope
                obj = self
                # Get the method
                method = str(req.method)
                # Get the "steps" to get there, i.e. what traversal to do
                if debug: print method
                steps = method.split('.')
                if debug: print steps

                # Iterate through the scope to find the final object
                for step in steps:
                    # Replace our current scope with the object specified in the request
                    obj = getattr(obj, step, None)
                    # Make sure that the object/scope exists
                    if obj is None:
                        # Throw and error if it does not exist
                        raise JsonRpcMethodNotFound("Could not find '%s' method" % req.method)

                # Execute the function and return the response
                ret = obj(**req.params)

                # Make the response
                resp = JsonRpcResponse()
                resp['id'] = req.id
                resp.load_success(ret)

                # Return the response
                return json.dumps(resp)
            except Exception as exc:
                if debug: traceback.print_exc()

                # Make the response
                errResp = JsonRpcResponse()
                errResp.load_error(exc)

                # Return the response
                return json.dumps(errResp)

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

        @app.route('/getProperties/', methods=['GET'])
        def get_properties():
            try:
                with open("/home/pi/info.json", "r") as in_json:
                    return json.dumps(json.load(in_json))
            except FileNotFoundError:
                return "File Not Found Error"
            except Exception as exception:
                return "Unknown error" + str(exception)

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
        self.board = BaseballBoard(self.rootView)
        #self.board = FakeBoard(self.rootView)

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
        return "Connected - OLD"

    def getProperties(self, dataStr=None):
        try:
            with open("/home/pi/info.json", "r") as in_json:
                return json.dumps(json.load(in_json))
        except FileNotFoundError:
            return "File Not Found Error"
        except Exception as exception:
            return "Unknown error" + str(exception)

    def clear(self, dataStr=None):
        self.rootView.removeAllViews()


if __name__ == '__main__':
    web = FlaskRPC()
    # time.sleep(.5)
    # web.startUpDelay()
    # print("Ran")
    #web.createBoot("null")

