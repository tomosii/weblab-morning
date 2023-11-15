def text():
    return f"新しい豆知識が追加されました！"


def blocks():
    return [
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": ":bulb: *新しい豆知識が追加されました！*",
                }
            ],
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": "朝活で時間通りに来た人にだけ教えちゃいます！",
                }
            ],
        },
    ]


def ephemeral_text():
    return f"豆知識を追加しました！"


def ephemeral_blocks(trivia_text: str):
    return [
        {
            "type": "section",
            "text": {
                "type": "plain_text",
                "text": "豆知識を追加しました！",
                "emoji": True,
            },
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "plain_text",
                    "text": trivia_text,
                    "emoji": True,
                }
            ],
        },
    ]
