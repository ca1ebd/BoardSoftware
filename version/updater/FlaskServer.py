#!/usr/bin/python

from flask import Flask, request
import json
from UpdateService import GitUpdateService
import traceback

class ReflectiveFlaskRPCServer():

    def __init__(self):
        self.updater = GitUpdateService('/home/pi/scoreboard-git', '/home/pi/updater/versions.json')
        self.app = self.createApp()
        self.app.run(host="0.0.0.0", port="8080", debug=False)

    def createApp(self):
        app = Flask(__name__)

        @app.route('/', methods=['GET', 'POST'])
        def rpc():
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

            resp = None
            try:
                if '.' in method:
                    obj = self
                    while '.' in method:
                        comps = method.split('.')
                        obj = getattr(obj, comps[0])
                        method = '.'.join(comps[1:])
                    resp = getattr(obj, method)(params)
                else:
                    resp = getattr(self, method)(params)
            except Exception as inst:
                print("ERROR ERROR ERROR ERROR ERROR")
                traceback.print_exc()
                print(inst)
                return '{"error", "Could not process your request!"}'

            ret = {"id": uid, "response": resp}
            return json.dumps(ret) # '{"id":"%s", "result":"%s"}' % (uid, resp)

        @app.route('/upload_pkg', methods=["POST"])
        def upload_pkg():
            self.updater.loadNewGit(request.files["update"])
            return '{"message": "Upload Successful!"}'

        @app.route('/upload_vers', methods=["POST"])
        def upload_vers():
            self.updater.loadNewVersions(request.files["versions"])
            return '{"message": "Upload Successful!"}'

        @app.route('/upload_full', methods=["POST"])
        def upload_full():
            print request.files
            self.updater.loadNewVersions(request.files["versions"])
            self.updater.loadNewGit(request.files["update"])
            return '{"message": "Upload Successful!"}'

        return app

    def test(self, params=None):
        return "TEST FUNC"

if __name__ == "__main__":
    web = ReflectiveFlaskRPCServer()