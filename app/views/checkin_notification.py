import datetime

from app.utils.time_difference import get_time_difference_str


def text(user_id: str):
    return f"<@{user_id}> さんがチェックインしました！"


def blocks(
    user_id: str,
    place_name: str,
    checkin_at: datetime.datetime,
    time_difference_seconds: int,
    total_points: int,
    point_change: int,
) -> list[dict]:
    checkin_time_text = checkin_at.strftime("%H:%M")
    time_diff_text = get_time_difference_str(time_difference_seconds)

    point_change_text = (
        f"+{int(point_change)}" if point_change > 0 else str(int(point_change))
    )

    return [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"<@{user_id}> さんがチェックインしました",
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
                {
                    "type": "mrkdwn",
                    "text": f":star: *`{point_change_text}pt`*",
                },
                {
                    "type": "mrkdwn",
                    "text": f"今週の合計 *{int(total_points)}pt*",
                },
            ],
        },
    ]
