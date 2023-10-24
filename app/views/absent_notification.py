def text(user_id: str):
    return f"<@{user_id}> さんから朝活のお休みの連絡がありました！"


def blocks(user_id: str, reason: str):
    return [
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": f"<@{user_id}> さんから朝活のお休みの連絡がありました！\n欠席理由: *{reason}*",
                }
            ],
        }
    ]
