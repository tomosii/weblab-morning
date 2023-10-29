import datetime

from app.utils import weekday
from app.models.commitment import UserCommitment


def text():
    return f"現在の得点の状況です！"


def blocks(winner_id: str, user_points):
    return [
        {
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "plain_text",
                        "text": "現在の得点の状況です！",
                        "emoji": True,
                    },
                },
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": ":trophy: 現在のランキング",
                        "emoji": True,
                    },
                },
                {"type": "divider"},
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": ":first_place_medal: 1位  *5pt*"},
                },
                {
                    "type": "rich_text",
                    "elements": [
                        {
                            "type": "rich_text_list",
                            "style": "bullet",
                            "indent": 0,
                            "border": 0,
                            "elements": [
                                {
                                    "type": "rich_text_section",
                                    "elements": [
                                        {"type": "user", "user_id": "U04QANYLPK6"}
                                    ],
                                },
                                {
                                    "type": "rich_text_section",
                                    "elements": [
                                        {"type": "user", "user_id": "U04QANYLPK6"}
                                    ],
                                },
                            ],
                        }
                    ],
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": ":second_place_medal: 2位   *2pt*",
                    },
                },
                {
                    "type": "rich_text",
                    "elements": [
                        {
                            "type": "rich_text_list",
                            "style": "bullet",
                            "indent": 0,
                            "border": 0,
                            "elements": [
                                {
                                    "type": "rich_text_section",
                                    "elements": [
                                        {"type": "user", "user_id": "U04QANYLPK6"}
                                    ],
                                },
                                {
                                    "type": "rich_text_section",
                                    "elements": [
                                        {"type": "user", "user_id": "U04QANYLPK6"}
                                    ],
                                },
                            ],
                        }
                    ],
                },
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": ":rotating_light: ペナルティ",
                        "emoji": True,
                    },
                },
                {"type": "divider"},
                {
                    "type": "rich_text",
                    "elements": [
                        {
                            "type": "rich_text_list",
                            "style": "bullet",
                            "indent": 0,
                            "border": 0,
                            "elements": [
                                {
                                    "type": "rich_text_section",
                                    "elements": [
                                        {"type": "user", "user_id": "U04QANYLPK6"},
                                        {"type": "text", "text": "   "},
                                        {
                                            "type": "text",
                                            "text": "3pt",
                                            "style": {"bold": True},
                                        },
                                    ],
                                },
                                {
                                    "type": "rich_text_section",
                                    "elements": [
                                        {"type": "user", "user_id": "U04QANYLPK6"},
                                        {"type": "text", "text": "   "},
                                        {
                                            "type": "text",
                                            "text": "1pt",
                                            "style": {"bold": True},
                                        },
                                    ],
                                },
                            ],
                        }
                    ],
                },
            ]
        }
    ]
