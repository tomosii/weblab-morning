import datetime

from ..utils import weekday
from ..models.commitment import UserCommitment


def text():
    return f"朝活参加者は以下の通りです！ :placard:"


def blocks(user_commits: list[UserCommitment]):
    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "今週の参加者 :sunglasses:",
                "emoji": True,
            },
        },
        {"type": "divider"},
    ]

    for commit in user_commits:
        dates_str = ", ".join(
            [
                weekday.get_jp_date_str(date=date, with_day_of_week=False)
                for date in commit.dates
            ]
        )
        blocks.append(
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": f"<@{commit.user_id}>",
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*{commit.time}*",
                    },
                ],
            }
        )
        blocks.append(
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": dates_str,
                    },
                ],
            },
        )

    return blocks
