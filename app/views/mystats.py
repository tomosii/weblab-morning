import datetime
from app.models.point import UserPoint, UserWinningTimes


def text(user_id: str):
    return f"<@{user_id}> さんのこれまでの朝活の振り返りです！"


def blocks(
    user_id: str,
    my_winning_times: int,
    my_joined_weeks_count: int,
    my_joined_days_count: int,
    my_points: UserPoint,
) -> list[dict]:
    print(f"My winning times: {my_winning_times}")
    print(f"My joined weeks count: {my_joined_weeks_count}")
    print(f"My joined days count: {my_joined_days_count}")
    print(f"My total point: {my_points.total_point}")
    print(f"My total penalty: {my_points.total_penalty}")

    _blocks = [
        {
            "type": "section",
            "text": {
                "type": "plain_text",
                "text": f"<@{user_id}> さんのこれまでの戦績です！",
                "emoji": True,
            },
        },
        {
            "type": "divider",
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": ":crown:  通算勝利回数",
                },
                {
                    "type": "mrkdwn",
                    "text": f"*{my_winning_times}勝*",
                },
                {
                    "type": "mrkdwn",
                    "text": ":bookmark:  通算参加週数",
                },
                {
                    "type": "mrkdwn",
                    "text": f"*{my_joined_weeks_count}週*",
                },
                {
                    "type": "mrkdwn",
                    "text": ":date:  通算参加日数",
                },
                {
                    "type": "mrkdwn",
                    "text": f"*{my_joined_days_count}日*",
                },
            ],
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": ":gem:  通算ポイント",
                },
                {
                    "type": "mrkdwn",
                    "text": f"*`{my_points.total_point}pt`*",
                },
                {
                    "type": "mrkdwn",
                    "text": ":pleading_face:  通算ペナルティ",
                },
                {
                    "type": "mrkdwn",
                    "text": f"*`{my_points.total_penalty}pt`*",
                },
            ],
        },
    ]

    return _blocks
