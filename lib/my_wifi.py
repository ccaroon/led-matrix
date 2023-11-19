import os
import socketpool
import ssl
import wifi

import adafruit_requests

class MyWiFi:
    REQUESTS = None

    @classmethod
    def connect(cls):
        essid = os.getenv("WIFI_SSID")
        passwd = os.getenv("WIFI_PASSWORD")

        print(f"Trying '{essid}'...")
        wifi.radio.connect(essid, passwd)

        if wifi.radio.connected:
            pool = socketpool.SocketPool(wifi.radio)
            cls.REQUESTS = adafruit_requests.Session(
                pool,
                ssl.create_default_context()
            )
            print("Connected to '%s'" % (essid))
        else:
            print("Failed to connect to '%s'" % (essid))

    @classmethod
    def autoconnect(cls):
        if wifi.radio.connected:
            print(f"Already connected to '{wifi.radio.ap_info.ssid}'")
        else:
            cls.connect()

    @classmethod
    def test(cls, url="http://api.open-notify.org/iss-now.json"):
        if wifi.radio.connected:
            resp = cls.REQUESTS.get(url)
            if resp.status_code == 200:
                return resp.json()
            else:
                return "Error GET'ting '%s': [%d]" % (url, resp.status_code)
        else:
            print("Not Connected")

    @classmethod
    def scan(cls):
        print("Available WiFi networks:")
        for network in wifi.radio.start_scanning_networks():
            print("\t%s\t\tRSSI: %d\tChannel: %d" % (str(network.ssid, "utf-8"),
                                                    network.rssi, network.channel))
        wifi.radio.stop_scanning_networks()

    @classmethod
    def check(cls):
        if wifi.radio.connected:
            print(f"Connected to '{wifi.radio.ap_info.ssid}'")
        else:
            print("Not Connected")
