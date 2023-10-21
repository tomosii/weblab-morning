command_not_found_text = "コマンドが見つかりませんでした。 `/morning help` でヘルプを表示します。"

blocks = [
    {
        "type": "rich_text",
        "elements": [
            {
                "type": "rich_text_section",
                "elements": [
                    {
                        "type": "text",
                        "text": "/morning コマンドの使い方は以下の通りです！\n",
                    },
                ],
            },
            {
                "type": "rich_text_list",
                "style": "bullet",
                "elements": [
                    {
                        "type": "rich_text_section",
                        "elements": [
                            {
                                "type": "text",
                                "text": "/morning commit",
                                "style": {"code": True},
                            },
                            {
                                "type": "text",
                                "text": ": 朝活の時間と日にちを設定します。",
                            },
                        ],
                    },
                    {
                        "type": "rich_text_section",
                        "elements": [
                            {
                                "type": "text",
                                "text": "/morning cancel",
                                "style": {"code": True},
                            },
                            {
                                "type": "text",
                                "text": ": 朝活への参加をキャンセルします。",
                            },
                        ],
                    },
                    {
                        "type": "rich_text_section",
                        "elements": [
                            {
                                "type": "text",
                                "text": "/morning commitments",
                                "style": {"code": True},
                            },
                            {
                                "type": "text",
                                "text": ": 今週の朝活参加者一覧を表示します。",
                            },
                        ],
                    },
                    {
                        "type": "rich_text_section",
                        "elements": [
                            {
                                "type": "text",
                                "text": "/morning summary",
                                "style": {"code": True},
                            },
                            {
                                "type": "text",
                                "text": ": 今週の朝活の結果を表示します。",
                            },
                        ],
                    },
                    {
                        "type": "rich_text_section",
                        "elements": [
                            {
                                "type": "text",
                                "text": "/morning leaderboard",
                                "style": {"code": True},
                            },
                            {
                                "type": "text",
                                "text": ": 累計のランキングを表示します。",
                            },
                        ],
                    },
                    {
                        "type": "rich_text_section",
                        "elements": [
                            {
                                "type": "text",
                                "text": "/morning help",
                                "style": {"code": True},
                            },
                            {
                                "type": "text",
                                "text": ": このヘルプを表示します。",
                            },
                        ],
                    },
                ],
            },
        ],
    },
]