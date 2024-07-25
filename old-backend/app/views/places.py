from ..models.place import Place


def text():
    return f"朝活のチェックイン場所一覧です！"


def blocks(places: list[Place]) -> list[dict]:
    _blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "チェックイン対応エリア一覧です！",
            },
        },
    ]

    for place in places:
        if place.enabled:
            _blocks.append(
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "mrkdwn",
                            "text": f":round_pushpin:  *{place.name}*",
                        }
                    ],
                }
            )
    return _blocks
