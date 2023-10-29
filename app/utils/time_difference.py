import datetime


def get_time_difference_str(seconds: float):
    text = ""
    abs_seconds = int(abs(seconds))

    hour = abs_seconds // 3600
    minute = (abs_seconds % 3600) // 60
    second = abs_seconds % 60

    if hour == 0 and minute == 0:
        text = f"{second}秒"
    elif hour == 0:
        text = f"{minute}分{second}秒"
    else:
        text = f"{hour}時間{minute}分"

    if seconds < 0:
        text = "-" + text
    else:
        text = "+" + text

    return text


def get_time_difference_seconds(commit_time: str, checkin_at: datetime.datetime):
    time_diff = checkin_at - checkin_at.replace(
        hour=int(commit_time.split(":")[0]),
        minute=int(commit_time.split(":")[1]),
        second=0,
        microsecond=0,
    )
    if time_diff < datetime.timedelta(0):
        time_diff_seconds = -(abs(time_diff).total_seconds())
    else:
        time_diff_seconds = time_diff.total_seconds()

    return time_diff_seconds
