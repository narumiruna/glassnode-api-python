from datetime import datetime


def to_timestamp(d: datetime) -> int:
    return int(d.timestamp())


def to_datetime(t: int) -> datetime:
    return datetime.fromtimestamp(t)
