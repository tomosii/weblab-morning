def text(user_id: str):
    return f"<@{user_id}> さんが朝活への参加を宣言しました！:fire:"


def blocks(
    user_id: str, commit_hours: int, commit_minutes: int, commit_days_labels: list
):
    return [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"<@{user_id}> さんが朝活への参加を宣言しました！:fire:",
            },
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f":clock10: *{commit_hours}時{commit_minutes}分*",
            },
        },
        {
            "type": "rich_text",
            "elements": [
                {
                    "type": "rich_text_list",
                    "style": "bullet",
                    "indent": 0,
                    "border": 1,
                    "elements": [
                        {
                            "type": "rich_text_section",
                            "elements": [
                                {
                                    "type": "text",
                                    "text": f"{day}",
                                    "style": {"code": True},
                                },
                            ],
                        }
                        for day in commit_days_labels
                    ],
                },
            ],
        },
    ]
