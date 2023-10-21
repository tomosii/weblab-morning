blocks = [
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": f"<@{payload['user']['id']}> さんが朝活への参加を表明しました！",
        },
    },
    {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": f"*{hour}時{minute}分*",
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
                            },
                        ],
                    }
                    for day in commit_days_label
                ],
            },
        ],
    },
]
