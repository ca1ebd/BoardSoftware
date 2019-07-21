#!/usr/bin/python

import sys

import json
import subprocess
import os.path
import zipfile


class GitUpdateService():

    def __init__(self, root_path, global_versions):
        # super(self)
        self.__git_path__ = root_path

        self.__global_path__ = global_versions
        self.__global_versions__ = json.loads(open(self.__global_path__).read())

        self.__current_path__ = root_path + '/version/version.json'

    def getCurrentVersion(self, path=None):
        # if path == None:
        path = self.__current_path__
        # print(self.__current_path__)
        version = json.loads(open(path).read())
        print(version)
        return version["version"]

    def getCurrentInfo(self, params=None):
        curr = json.loads(open(self.__current_path__).read())
        j = {"current": curr, "global": self.__global_versions__}
        return json.dumps(j)

    def loadNewGit(self, f):
        current_num = self.getCurrentVersion()

        #TODO: REPLACE ROOT DIR WITH THE CURRENT DIR FROM SYS
        rootDir = '/home/pi/updater/'
        interDir = rootDir + 'inter/'
        subprocess.call("mkdir " + interDir, shell=True)
        f.save(interDir + "update.zip")
        zipRef = zipfile.ZipFile(interDir + "update.zip", 'r')
        zipRef.extractall(self.__git_path__)
        zipRef.close()
        subprocess.call("rm -rf " + interDir[:-1], shell=True)

        print self.__global_versions__
        versions = self.__global_versions__["versions"]
        print versions

        for vers in versions:
            if vers["board_version"] == current_num:
                subprocess.call("cd " + self.__git_path__ + " && git stash && git checkout " + vers["sha-key"], shell=True)
                break

        self.goToVersion(self.__global_versions__['latest'])

    def loadNewVersions(self, f):
        f.save(self.__global_path__)
        self.__global_versions__ = json.loads(open(self.__global_path__).read())

    def goToProtocol(self, params):
        max_ver = int(0)

        protocol = -1
        if type(params) == int:
            protocol = params
        elif type(params) == str:
            try:
                j = json.loads(params)
                protocol = int(j["protocol"])
            except:
                protocol = int(params)
        elif type(params) == dict:
            protocol = int(params["protocol"])

        print("Searching for version compatible with protocol: %d" % protocol)
        for v in self.__global_versions__["versions"]:
            if int(v["protocol_version"]) == protocol:
                if int(v["board_version"]) > max_ver:
                    max_ver = int(v["board_version"])
        print("Found version %d!" % max_ver)

        self.goToVersion(max_ver)


    def goToVersion(self, version_num):
        versions = self.__global_versions__["versions"]

        try:
            current_num = int(self.getCurrentVersion())
        except Exception:
            print("ERROR!")
            print("Could not find the current version!")
            return

        next_version_num = None
        if version_num == current_num:
            print 'Already at target version!'
            return
        elif version_num > current_num:
            next_version_num = current_num + 1
        else:
            next_version_num = current_num - 1

        print 'Target Version: ' + str(version_num)
        print 'Current Version: ' + str(current_num)
        print 'Searching for Version: ' + str(next_version_num)

        next_version = None
        for version in versions:
            if version["board_version"] == next_version_num:
                next_version = version
                break

        if next_version == None:
            print 'ERROR!'
            print 'Could not find a compatible version!'
            return

        if next_version_num < current_num:
            if os.path.isfile(self.__git_path__ + '/version/down'):
                ret = subprocess.call("cd " + self.__git_path__ + "/version/ && chmod +x down && ./down", shell=True)
                if ret < 0:
                    print("ERROR %d, Could not execute the 'down' script!" % ret)
                    return

        sha = next_version["sha-key"]
        ret = subprocess.call("cd " + self.__git_path__ + " && git stash && git checkout " + sha, shell=True)
        if ret < 0 or ret == 128:
            print("ERROR %d, Could not change the git version!" % ret)
            return

        if next_version_num > current_num:
            if os.path.isfile(self.__git_path__ + '/version/up'):
                ret = subprocess.call("cd " + self.__git_path__ + "/version/ && chmod +x up && ./up", shell=True)
                if ret < 0:
                    print("ERROR %d, Could not execute the 'up' script!" % ret)
                    return

        if next_version_num != version_num:
            self.goToVersion(version_num)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print 'ERROR: Only received %d arguments!' % len(sys.argv)
        print 'Usage: python UpdateService.py [root_dir] [version_file] [version_number]'
        exit()

    root_dir = sys.argv[1]
    version_file = sys.argv[2]
    version_num = sys.argv[3]
    print 'Setting ' + root_dir + ' to version #' + version_num

    updater = GitUpdateService(root_dir, version_file)
    updater.goToVersion(int(version_num))
