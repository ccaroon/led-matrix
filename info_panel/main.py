import os
from my_wifi import MyWiFi
from chronos import Chronos

MyWiFi.autoconnect()
Chronos.sync(tz_offset=os.getenv("TZ_OFFSET"))
Chronos.test()
