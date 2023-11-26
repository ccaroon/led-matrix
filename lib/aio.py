import re
import os
import time

from chronos import Chronos

class AdafruitIO:
    BASE_URL = "https://io.adafruit.com/api/v2"

    def __init__(self, requests, group, config:dict):
        self.__username = config.get("username")
        self.__key      = config.get("key")
        self.__requests = requests
        self.__group_name = group

    def get_data(self, feed, **kwargs):
        feed_name = f"{self.__group_name}.{feed}"

        limit = kwargs.get('limit', 1)
        fields = ["value", "created_at"]
        fields.extend(kwargs.get('fields', []))
        include = ','.join(fields)
        url = f"{AdafruitIO.BASE_URL}/{self.__username}/feeds/{feed_name}/data?limit={limit}&include={include}"

        headers = {'X-AIO-Key': self.__key}

        resp = self.__requests.get(url, headers=headers)

        if resp.status_code == 200:
            results = resp.json()
            output = {
                "success": True,
                "results" : results,
                "created_at": Chronos.format_time(self.__parse_dt(results[0]["created_at"])),
                "age": self.__data_age(results[0]["created_at"])
            }
        else:
            output = {
                "success": False,
                "code": resp.status_code,
                "feed": feed_name,
                "msg": resp.json()['error']
            }

        return (output)

    def __parse_dt(self, date_str):
        # 2023-01-28T20:45:31Z - UTC
        match = re.match("(\d\d\d\d)-(\d\d)-(\d\d)T(\d\d):(\d\d):(\d\d)Z", date_str)
        time_t = (
            # YYYY, MM, DD
            int(match.group(1)), int(match.group(2)), int(match.group(3)),
            # HH, MM, SS
            int(match.group(4)), int(match.group(5)), int(match.group(6)),
            # WDay, YDayt, isDST
            0, 0, -1
        )

        time_e = time.mktime(time_t)

        # Adjust for timezone & DST
        offset = os.getenv("time.tz_offset")
        if Chronos.is_dst():
            offset += 1

        # offset hours in seconds
        time_e += offset * (60 * 60)

        return time_e

    def __data_age(self, date_str):
        time_e = self.__parse_dt(date_str)
        now = time.mktime(time.localtime())

        return now - time_e

    def handle_response(self, resp):
        if resp['success'] and resp.get('dry_run', False):
            results = resp['results']
            print(f"DRY RUN: [{results['data']['value']}] -> {results['url']}")
        elif resp['success']:
            results = resp['results']
            print(f"{results['id']} - {results['feed_key']}: [{results['value']}]")
        else:
            error_msg = f"AIO: [{resp['value']}] -> [{resp['feed']}] | {resp['code']} - {resp['msg']}"
            raise Exception(error_msg)
