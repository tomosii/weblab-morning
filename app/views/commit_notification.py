import datetime

from app.utils import weekday


def text(user_id: str):
    return f"<@{user_id}> さんが朝活への参加を宣言しました！:fire:"


def blocks(user_id: str, commit_time: str, commit_dates: list[datetime.date]):
    hour = commit_time.split(":")[0]
    minute = commit_time.split(":")[1]
    dates_with_commas = ",  ".join(
        [
            weekday.get_jp_date_str(date=date, with_day_of_week=False)
            for date in commit_dates
        ]
    )

    return [
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": f"<@{user_id}> さんが朝活参加を宣言しました！",
                },
            ],
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": f":clock10:  *{hour}時{minute}分*",
                },
            ],
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": dates_with_commas,
                },
            ],
        },
    ]
