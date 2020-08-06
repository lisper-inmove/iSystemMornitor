# -*- coding: utf-8 -*-


from datetime import datetime
import pytz
import tzlocal


class DateUtils:
    def __init__(self):
        pass

    @property
    def utc(self):
        return pytz.timezone("UTC")

    @property
    def local(self):
        return tzlocal.get_localzone()

    @property
    def default_fmt(self):
        return "%Y-%m-%d %H:%M:%S"

    def timestamp_to_string(self, timestamp, fmt=None):
        if fmt is None:
            fmt = self.default_fmt
        date = datetime.fromtimestamp(timestamp)
        date = date.astimezone(self.local).strftime(fmt)
        return date
