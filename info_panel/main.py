import os
from aio import AdafruitIO
from my_wifi import MyWiFi
from chronos import Chronos

MyWiFi.autoconnect()
# MyWiFi.test()

Chronos.sync(tz_offset=os.getenv("time.tz_offset"))
# Chronos.test()
# Chronos.is_dst()

aio = AdafruitIO(
    MyWiFi.REQUESTS,
    "weather-station",
    { "username": os.getenv("aio.username"), "key": os.getenv("aio.key")})

resp = aio.get_data("temperature")
if resp['success']:
    temp = int(resp["results"][0]["value"])
    cat = resp["created_at"]

    print(f"{temp} @ {cat} [{resp['age']}]")
