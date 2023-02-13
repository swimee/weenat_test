from enum import Enum


class SpanValues(Enum):
    """agregate data given this parameters"""

    DAY = "day"
    HOUR = "hour"
    MAX = "max"
    RAW = ""


class LabelField:
    """name of the metrics"""

    TEMP = "temp"
    PRECIP = "precip"
    HUM = "hum"
