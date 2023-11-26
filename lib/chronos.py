import os
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

    @classmethod
    def format_time(cls, seconds):
        lt = time.localtime(seconds)

        return f"{lt.tm_year:04d}-{lt.tm_mon:02d}-{lt.tm_mday:02d} @ {lt.tm_hour:02d}:{lt.tm_min:02d}:{lt.tm_sec:02d}"

    @classmethod
    def is_dst(cls):
        is_dst = False
        now = time.localtime()
        date_code = (now.tm_mon * 100) + now.tm_mday

        # GET DST table for current year
        dst_period = os.getenv(f"time.dst.{now.tm_year}").split(":", 2)

        if date_code >= int(dst_period[0]) and date_code <= int(dst_period[1]):
            is_dst = True

        # print(f"DCode: {date_code} | DST? {is_dst} | DST from {dst_period[0]} to {dst_period[1]}")

        return is_dst
