import datetime

from app.utils import weekday
from app.models.point import Point


def text():
    return f"今週の朝活勝者の発表です！"


def blocks(winner_id: str, user_points: list[Point]) -> list[dict]:
    _blocks = [
        {
            "type": "section",
            "text": {
                "type": "plain_text",
                "text": "1週間お疲れ様でした！",
                "emoji": True,
            },
        },
        {
            "type": "section",
            "text": {
                "type": "plain_text",
                "text": "今週の朝活の勝者は ....",
                "emoji": True,
            },
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f":trophy: <@{winner_id}> さんです！！:tada:",
            },
        },
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": ":star: 結果",
                "emoji": True,
            },
        },
        {"type": "divider"},
        {
            "type": "section",
            "fields": [
                {"type": "mrkdwn", "text": "<@U04QANYLPK6>"},
                {"type": "mrkdwn", "text": "*`2pt`*"},
            ],
        },
        {
            "type": "section",
            "fields": [
                {"type": "mrkdwn", "text": "<@U039S8P0B9T>"},
                {"type": "mrkdwn", "text": "*`2pt`*  (-2pt)"},
            ],
        },
        {
            "type": "section",
            "fields": [
                {"type": "mrkdwn", "text": "<@U04Q5BG479T>"},
                {"type": "mrkdwn", "text": "*`2pt`*"},
            ],
        },
    ]

    for point in user_points:
        point_text = f"*`{point.point}pt`*"
        if point.penalty < 0:
            point_text += f"  ({point.penalty}pt)"

        _blocks.append(
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"<@{point.user_id}>"},
                    {"type": "mrkdwn", "text": point_text},
                ],
            }
        )

    return _blocks
