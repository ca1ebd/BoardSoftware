from flask import Flask, request
import subprocess
import zipfile


class Update:
    def __init__(self):
        self.app = self.createApp()
        self.app.debug = True
        self.app.run(host='0.0.0.0', port=5000)

    def createApp(self):
        app = Flask(__name__)

        @app.route('/update/', methods=['POST'])
        def update():
            try:
                f = request.files['update']
                dir = '/home/pi/scoreboard/scoreboard/update/work/'
                # newDir = os.path.dirname(dir)
                # os.makedirs(newDir)
                # os.system("mkdir " + dir)
                try:
                    subprocess.call('mkdir ' + dir, shell=True)
                except Exception:
                    print("excepted")
                    subprocess.call('rm -rf ' + dir, shell=True)
                    subprocess.call('mkdir ' + dir, shell=True)

                zipName = 'update.zip'
                f.save(dir + zipName)
                zipRef = zipfile.ZipFile(dir + zipName, 'r')
                zipRef.extractall(dir)
                zipRef.close()
                subprocess.call('')
                subprocess.call('cd ' + dir + ' && sh ' + dir + 'update.sh > log.txt',
                                shell=True)
                subprocess.call('rm -rf ' + dir, shell=True)
            except Exception:
                return '{"Status":"Fail"}'
                #TODO would like to return exception
            return '{"Status":"OK"}'

        return app


if __name__ == '__main__':
    web = Update()