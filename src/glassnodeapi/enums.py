from enum import Enum


class FrequencyInterval(str, Enum):
    TEN_MINUTES = "10m"
    ONE_HOUR = "1h"
    ONE_DAY = "24h"
    ONE_WEEK = "1w"
    ONE_MONTH = "1month"


class Format(str, Enum):
    JSON = "json"
    CSV = "csv"


class TimestampFormat(str, Enum):
    UNIX = "unix"
    HUMANIZED = "humanized"  # RFC 3339
