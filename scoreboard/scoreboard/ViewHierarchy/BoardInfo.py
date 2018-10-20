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