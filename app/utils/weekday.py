import datetime
import jpholiday

jp_days_of_week = {
    0: "月",
    1: "火",
    2: "水",
    3: "木",
    4: "金",
    5: "土",
    6: "日",
}


def is_jp_weekday(date: datetime.date) -> bool:
    return date.weekday() < 5 and not jpholiday.is_holiday(date)


def get_jp_date_str(date: datetime.date, with_day_of_week: bool = True) -> str:
    if with_day_of_week:
        return f"{date.month}/{date.day} ({get_jp_day_of_week(date)})"
    else:
        return f"{date.month}/{date.day}"


def get_next_weekdays() -> list[datetime.date]:
    today = datetime.date.today()

    # Get weekdays of the next week (next Monday to Friday)
    if today.weekday() == 0:
        next_monday = today + datetime.timedelta(days=7)
    else:
        next_monday = today + datetime.timedelta(days=7 - today.weekday())

    next_weekdays = []
    for i in range(5):
        day = next_monday + datetime.timedelta(days=i)
        if is_jp_weekday(day):
            next_weekdays.append(day)
    print("Next weekdays:", next_weekdays)

    return next_weekdays


def get_jp_day_of_week(date: datetime.date) -> str:
    return jp_days_of_week[date.weekday()]


if __name__ == "__main__":
    get_next_weekdays()
