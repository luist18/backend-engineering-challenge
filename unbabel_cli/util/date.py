from datetime import datetime, timedelta


def floor_minute(date: datetime) -> datetime:
    return date.replace(second=0, microsecond=0)


def ceil_minute(date: datetime) -> datetime:
    return (date + timedelta(minutes=1)).replace(second=0, microsecond=0)
