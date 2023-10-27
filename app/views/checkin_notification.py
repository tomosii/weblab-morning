import datetime

from app.utils.time_difference import get_time_difference_str


def text(user_id: str):
    return f"<@{user_id}> さんがチェックインしました！"


def blocks(
    user_id: str,
    place_name: str,
    checkin_at: datetime.datetime,
    time_difference_seconds: int,
) -> list[dict]:
    checkin_time_text = checkin_at.strftime("%H:%M")
    time_diff_text = get_time_difference_str(time_difference_seconds)

    return [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"<@{user_id}> さんがチェックインしました！:sunny:",
            },
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": f"*{place_name}*  {checkin_time_text} ({time_diff_text})",
                }
            ],
        },
        {
            "type": "section",
            "fields": [
                {"type": "mrkdwn", "text": ":candy: `*+1pt*`"},
                {"type": "mrkdwn", "text": ":star: 合計 *4pt*"},
            ],
        },
    ]
