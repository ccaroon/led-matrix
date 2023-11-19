import time

import rtc
import socketpool
import wifi

import adafruit_ntp

class Chronos:
    @classmethod
    def sync(cls, tz_offset=0):
        if wifi.radio.connected:
            pool = socketpool.SocketPool(wifi.radio)
            ntp = adafruit_ntp.NTP(pool, tz_offset=tz_offset)
            rtc.RTC().datetime = ntp.datetime
        else:
            raise RuntimeError("Cannot Sync Time. WiFi not connected!")

    @classmethod
    def test(cls, count=10):
        for _ in range(count):
            tdata = time.localtime()
            print(f"{tdata.tm_year}-{tdata.tm_mon}-{tdata.tm_mday} {tdata.tm_hour}:{tdata.tm_min}:{tdata.tm_sec}")
            time.sleep(1)
