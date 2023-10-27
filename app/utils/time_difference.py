def get_time_difference_str(seconds: int):
    text = ""
    abs_seconds = abs(seconds)

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
