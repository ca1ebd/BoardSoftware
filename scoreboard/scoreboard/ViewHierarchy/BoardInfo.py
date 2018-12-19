import json
from config import *

def GetWifiInfo():
    data = []
    dataFile = open("/etc/hostapd/hostapd.conf", "r")
    for line in dataFile:
        split = line.rstrip().split('=')
        data.append(split)

    return data

def GetWifiConnectionInfo():
    data = GetWifiInfo()
    ssid = ""
    password = ""
    for i in range(0, len(data)):
        if data[i][0] == 'ssid':
            ssid = data[i][1]
        elif data[i][0] == 'wpa_passphrase':
            password = data[i][1]
    return (ssid, password)

def generateInfo():
    json_dict = {
        "ssid": "blank_ssid",
        "password": "blank_password",
        "panelType": -1,
        "version": -1,
        "proto": -1
    }

    (json_dict['ssid'], json_dict['password']) = GetWifiConnectionInfo()
    if json_dict['ssid'].upper() in legacy_panel_ssids:
        json_dict['panelType'] = 1
    else:
        json_dict['panelType'] = 2


    for key in json_dict:
        print("{0}: {1}".format(key, json_dict[key]))

    with open('/home/pi/info.json', 'w') as json_out:
        json.dump(json_dict, json_out, indent=1)
