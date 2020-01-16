import datetime
import re


def parse_iso8601(timestamp: str) -> datetime.datetime:
    """Parse an ISO-8601 formatted time stamp."""
    timestamp = timestamp.strip()

    with_microseconds_colons: str = "(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})\.(\d{1,6})Z?"
    with_microseconds: str = "(\d{4})(\d{2})(\d{2})T(\d{2})(\d{2})(\d{2})\.(\d{1,6})Z?"
    with_seconds_colons: str = "(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})Z?"
    with_seconds: str = "(\d{4})(\d{2})(\d{2})T(\d{2})(\d{2})(\d{2})Z?"
    with_minutes_colons: str = "(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2})Z?"
    with_minutes: str = "(\d{4})(\d{2})(\d{2})T(\d{2})(\d{2})Z?"
    with_hours_colons: str = "(\d{4})-(\d{2})-(\d{2})T(\d{2})Z?"
    with_hours: str = "(\d{4})(\d{2})(\d{2})T(\d{2})Z?"
    date_only_pattern_dashes: str = "(\d{4})-(\d{2})-(\d{2})Z?"
    date_only_pattern: str = "(\d{4})(\d{2})(\d{2})Z?"

    found = False
    year, month, day, hour, minute, second, microsecond = [999] * 7
    for pattern in [
        with_microseconds_colons,
        with_microseconds,
        with_seconds_colons,
        with_seconds,
        with_minutes_colons,
        with_minutes,
        with_hours_colons,
        with_hours,
        date_only_pattern_dashes,
        date_only_pattern,
    ]:
        pattern_compiled = re.compile(pattern)
        match_range = pattern_compiled.fullmatch(timestamp)
        # Check if the match covers the whole input string
        if match_range and match_range.pos == 0 and match_range.endpos == len(timestamp):
            found = True
            match_groups = pattern_compiled.findall(timestamp)
            groups_as_list = [x for x in match_groups[0]]
            # Fill missing regex groups with zeros (hours, minutes, seconds, microseconds)
            for _ in range(7 - len(groups_as_list)):
                groups_as_list.append("0")
            # Append trailing zeros to microseconds
            while len(groups_as_list[-1]) < 6:
                groups_as_list[-1] = groups_as_list[-1] + "0"
            groups_as_list = [int(x) for x in groups_as_list]
            year, month, day, hour, minute, second, microsecond = groups_as_list

    if not found:
        raise ValueError(
            f"Could not parse timestamp: {timestamp}\nIt needs to be in the format 'yyyy-mmm-ddThh:mm:ss.ssss' or 'yyyymmddThhmmss.ssss' and it can omit microseconds, microseconds and seconds, microseconds and seconds and minutes, or microseconds and seconds and minutes and hours."
        )

    if month == 0:
        raise ValueError(f"Month must start at 1! Given month was: {month}")

    if day == 0:
        raise ValueError(f"Day must start at 1! Given day was: {day}")

    if month > 12:
        raise ValueError(f"There are only 12 months (including)! Given month was: {month}")

    day_limit_per_month = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 30, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
    if day > day_limit_per_month[month]:
        raise ValueError(
            f"The month {month} can at most have {day_limit_per_month[month]} days (including)! Given day was: {day}"
        )

    if day > 31:
        raise ValueError(f"A month can have at most 31 days (including)! Given day was: {day}.")

    if hour > 23:
        raise ValueError(f"A day can have at most 24 hours (excluding)! Given hour was: {hour}.")

    if minute > 59:
        raise ValueError(f"An hour can have at most 60 minutes (excluding)! Given minute was: {minute}.")

    if second > 59:
        raise ValueError(f"A minute can have at most 60 seconds (excluding)! Given second was: {second}.")
    # Doesn't need microsecond ValueError because the regex string can only detect range [0, 999_999]

    return datetime.datetime(
        year=year, month=month, day=day, hour=hour, minute=minute, second=second, microsecond=microsecond
    )

    # d = datetime.datetime(
    #     year=year, month=month, day=day, hour=hour, minute=minute, second=second, microsecond=microsecond
    # )
    # print(timestamp, d)
    # return d


if __name__ == "__main__":
    pass
    # parse_iso8601("asd")
    parse_iso8601("20190101T00")
    # parse_iso8601("2019-1012")
    parse_iso8601("20170506")
    parse_iso8601("20170506T12")
    parse_iso8601("2017-05-06T12:01:23.456")
    parse_iso8601("2017-05-06T12:01:23.0456")
    parse_iso8601("2017-05-06T12:01:23.123456")
