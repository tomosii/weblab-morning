def text(user_id: str):
    return f"<@{user_id}> さんが朝活の参加をキャンセルしました！"


def blocks(user_id: str):
    return [
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": f"<@{user_id}> さんが朝活の参加をキャンセルしました！",
                }
            ],
        }
    ]
