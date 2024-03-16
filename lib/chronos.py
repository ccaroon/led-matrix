import os
import time

import rtc
import socketpool
import wifi

import adafruit_ntp

class Chronos:
    MONTHS = (
        {"short": "Jan", "long": "January"},
        {"short": "Feb", "long": "February"},
        {"short": "Mar", "long": "March"},
        {"short": "Apr", "long": "April"},
        {"short": "May", "long": "May"},
        {"short": "Jun", "long": "June"},
        {"short": "Jul", "long": "July"},
        {"short": "Aug", "long": "August"},
        {"short": "Sep", "long": "September"},
        {"short": "Oct", "long": "October"},
        {"short": "Nov", "long": "November"},
        {"short": "Dec", "long": "December"}
    )

    # HINT: 11 chars per line for 48 pixel LED
    HOLIDAYS = {
        100: "1234567890+ 1234567890+",
        101: "Happy New Year",
        126: "Happy BDay, Piper",
        214: "Valentine's Day",
        219: "Happy BDay, Craig",
        316: "Cate+Craig Anniversary",
        317: "St. Patty's Day",
        704: "Happy July 4th",
        818: "Happy BDay, Nathan",
        823: "Happy BDay, Cate",
        1025: "Happy BDay, Picasso",
        1031: "Happy Halloween",
        # Not *exactly* the correct day, but close enough :)
        1125: "Happy Thksgiving",
        1224: "Christmas Eve",
        1225: "Merry Christmas",
        1231: "New Year's Eve"
    }

    @classmethod
    def sync(cls, tz_offset=0):
        if wifi.radio.connected:
            pool = socketpool.SocketPool(wifi.radio)
            ntp = adafruit_ntp.NTP(pool, tz_offset=tz_offset)
            rtc.RTC().datetime = ntp.datetime

            # Adjust for DST if necessary (after dt has been set)
            if cls.is_dst():
                dt_fields = list(ntp.datetime)
                # Add 1 to hour
                dt_fields[3] += 1
                rtc.RTC().datetime = time.struct_time(dt_fields)
        else:
            raise RuntimeError("Cannot Sync Time. WiFi not connected!")

    @classmethod
    def test(cls, count=10):
        for _ in range(count):
            tdata = time.localtime()
            print(f"{tdata.tm_year}-{tdata.tm_mon}-{tdata.tm_mday} {tdata.tm_hour}:{tdata.tm_min}:{tdata.tm_sec}")
            time.sleep(1)

    @classmethod
    def datetime_str(cls, seconds=None):
        lt = time.localtime(seconds)

        return f"{lt.tm_year:04d}-{lt.tm_mon:02d}-{lt.tm_mday:02d} @ {lt.tm_hour:02d}:{lt.tm_min:02d}:{lt.tm_sec:02d}"

    @classmethod
    def date_str(cls, **kwargs):
        mon_len = kwargs.get("mon_len", "short")
        now = time.localtime()
        month_name = cls.MONTHS[now.tm_mon-1][mon_len]
        # December 16, 2023
        return f"{month_name} {now.tm_mday:02d}, {now.tm_year}"

    @classmethod
    def date_code(cls):
        now = time.localtime()
        month = now.tm_mon
        day = now.tm_mday

        return (month * 100) + day

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

    @classmethod
    def motd(cls):
        date_code = cls.date_code()
        return cls.HOLIDAYS.get(date_code, cls.date_str())
