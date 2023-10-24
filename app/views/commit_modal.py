def commit_modal_view(days: list):
    return {}


modal_view = {
    "type": "modal",
    "title": {"type": "plain_text", "text": "朝活の参加表明"},
    "submit": {"type": "plain_text", "text": "確定"},
    "close": {"type": "plain_text", "text": "閉じる"},
    "blocks": [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": ":clock10:  時間の設定",
                "emoji": True,
            },
        },
        {
            "type": "input",
            "block_id": "commit-time-block",
            "element": {
                "type": "timepicker",
                "initial_time": "10:00",
                "action_id": "commit-time-action",
            },
            "label": {"type": "plain_text", "text": "今週は何時に設定しますか？"},
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "plain_text",
                    "text": "数字を直接入力すると細かい時間指定ができます！",
                    "emoji": True,
                }
            ],
        },
        {"type": "divider"},
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": ":date:  曜日の設定",
                "emoji": True,
            },
        },
        {
            "type": "input",
            "block_id": "commit-days-block",
            "label": {
                "type": "plain_text",
                "text": "どの日に参加しますか？",
            },
            "element": {
                "type": "checkboxes",
                "action_id": "commit-days-action",
                "options": [
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "10/16 (月)",
                            "emoji": True,
                        },
                        "value": "2023-10-16",
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "10/17 (火)",
                            "emoji": True,
                        },
                        "value": "2023-10-17",
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "10/18 (水)",
                            "emoji": True,
                        },
                        "value": "2023-10-18",
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "10/19 (木)",
                            "emoji": True,
                        },
                        "value": "2023-10-19",
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "10/20 (金)",
                            "emoji": True,
                        },
                        "value": "2023-10-20",
                    },
                ],
                "initial_options": [
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "10/16 (月)",
                        },
                        "value": "2023-10-16",
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "10/17 (火)",
                        },
                        "value": "2023-10-17",
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "10/18 (水)",
                        },
                        "value": "2023-10-18",
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "10/19 (木)",
                        },
                        "value": "2023-10-19",
                    },
                    {
                        "text": {
                            "type": "plain_text",
                            "text": "10/20 (金)",
                        },
                        "value": "2023-10-20",
                    },
                ],
            },
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": "この機能はまだ開発中です！:pray:",
                },
                {
                    "type": "mrkdwn",
                    "text": "~お休みの日があればチェックを外してください！~",
                },
            ],
        },
    ],
}
