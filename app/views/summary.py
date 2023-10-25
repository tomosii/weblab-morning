import datetime

from app.utils import weekday
from app.models.commitment import UserCommitment


def text():
    return f"今週の朝活勝者の発表です！"


def blocks(winner_id: str, user_points):
    return [
        {
            "type": "section",
            "text": {
                "type": "plain_text",
                "text": "1週間お疲れ様でした！:infinity-clap:",
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
            "text": {"type": "mrkdwn", "text": ":trophy: <@U04QANYLPK6> さんです！！:tada:"},
        },
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": ":placard: 結果",
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
