import datetime

from ..utils import weekday


def text(user_id: str):
    return f"<@{user_id}> さんが朝活の参加をキャンセルしました！"


def blocks(user_id: str, cancel_dates: list[datetime.date]):
    duration = f"{weekday.get_jp_date_str(date=cancel_dates[0], with_day_of_week=False,)} 〜 {weekday.get_jp_date_str(date=cancel_dates[-1], with_day_of_week=False,)}"
    return [
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": f"<@{user_id}> さんが朝活の参加をキャンセルしました！\n({duration})",
                }
            ],
        }
    ]
