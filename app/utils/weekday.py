import datetime
import jpholiday
from zoneinfo import ZoneInfo

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


def get_next_coming_weekdays() -> list[datetime.date]:
    """
    まだ開始されていない開催日を返す
    (commitmentの登録などに使う)
    """
    today = datetime.datetime.now(ZoneInfo("Asia/Tokyo")).date()

    # 今週の月曜日から金曜日のうち、平日の日付を取得
    this_monday = today - datetime.timedelta(days=today.weekday())
    this_weekdays = []
    for i in range(5):
        date = this_monday + datetime.timedelta(days=i)
        if is_jp_weekday(date):
            this_weekdays.append(date)
    print("This weekdays:", this_weekdays)

    # 今週の開催がまだ始まっていなければ、今週の開催日を返す
    if len(this_weekdays) != 0 and today < this_weekdays[0]:
        return this_weekdays

    # 今週の開催が始まっている場合は、次回の開催日を返す
    next_monday = this_monday + datetime.timedelta(days=7)
    next_weekdays = []
    for i in range(5):
        date = next_monday + datetime.timedelta(days=i)
        if is_jp_weekday(date):
            next_weekdays.append(date)
    print("Next weekdays:", next_weekdays)

    return next_weekdays


def get_ongoing_or_coming_weekdays() -> list[datetime.date]:
    """
    開催中なら開催中の日付を，開催中でなければ次の開催日を返す
    (参加者一覧の確認などに使う)
    """
    today = datetime.datetime.now(ZoneInfo("Asia/Tokyo")).date()

    # 今週の月曜日から金曜日のうち、平日の日付を取得
    this_monday = today - datetime.timedelta(days=today.weekday())
    this_weekdays = []
    for i in range(5):
        date = this_monday + datetime.timedelta(days=i)
        if is_jp_weekday(date):
            this_weekdays.append(date)
    print("This weekdays:", this_weekdays)

    # 今週の開催がまだ終わっていなければ、今週の開催日を返す
    if len(this_weekdays) != 0 and today <= this_weekdays[-1]:
        return this_weekdays

    # 今週の開催が終わっている場合は、次回の開催日を返す
    next_monday = this_monday + datetime.timedelta(days=7)
    next_weekdays = []
    for i in range(5):
        date = next_monday + datetime.timedelta(days=i)
        if is_jp_weekday(date):
            next_weekdays.append(date)
    print("Next weekdays:", next_weekdays)
    return next_weekdays


def get_ongoing_or_last_weekdays() -> list[datetime.date]:
    """
    開催中なら開催中の日付を，開催中でなければ前回の開催日を返す
    (結果の確認などに使う)
    """
    today = datetime.datetime.now(ZoneInfo("Asia/Tokyo")).date()

    # 今週の月曜日から金曜日のうち、平日の日付を取得
    this_monday = today - datetime.timedelta(days=today.weekday())
    this_weekdays = []
    for i in range(5):
        date = this_monday + datetime.timedelta(days=i)
        if is_jp_weekday(date):
            this_weekdays.append(date)
    print("This weekdays:", this_weekdays)

    # 今週の開催がもう始まっていれば、今週の開催日を返す
    if len(this_weekdays) != 0 and this_weekdays[0] <= today:
        return this_weekdays

    # まだ開催されていない場合は、前回の開催日を返す
    last_monday = this_monday - datetime.timedelta(days=7)
    last_weekdays = []
    for i in range(5):
        date = last_monday + datetime.timedelta(days=i)
        if is_jp_weekday(date):
            last_weekdays.append(date)
    print("Last weekdays:", last_weekdays)
    return last_weekdays


def get_jp_day_of_week(date: datetime.date) -> str:
    return jp_days_of_week[date.weekday()]


if __name__ == "__main__":
    pass
