import time

class Dates:
    MONTHS = (
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December"
    )

    HOLIDAYS = {
        101: "Happy New Year",
        126: "Happy BDay, Piper",
        214: "Happy Valentine's Day",
        219: "Happy BDay, Craig",
        316: "Happy Anniversary, CNC",
        317: "Happy St. Patrick's Day",
        704: "Happy July 4th",
        823: "Happy BDay, Cate",
        818: "Happy BDay, Nathan",
        1025: "Happy BDay, Picasso",
        1031: "Happy Halloween",
        # Not *exactly* the correct day, but close enough :)
        1125: "Happy Thanksgiving",
        1224: "Christmas Eve",
        1225: "Merry Christmas"
    }

    @classmethod
    def date_str(cls):
        now = time.localtime()
        month_name = cls.MONTHS[now.tm_mon-1]
        # December 16, 2023
        return f"{month_name} {now.tm_mday:02d}, {now.tm_year}"

    @classmethod
    def date_code(cls):
        now = time.localtime()
        month = now.tm_mon
        day = now.tm_mday

        return (month * 100) + day

    @classmethod
    def message(cls):
        date_code = cls.date_code()

        return cls.HOLIDAYS.get(date_code, cls.date_str())
