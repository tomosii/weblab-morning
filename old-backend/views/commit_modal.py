import datetime
from utils import weekday


def modal_view(activity_dates: list[datetime.date]) -> dict:
    print("Activity dates:", activity_dates)
    options = [
        {
            "text": {
                "type": "plain_text",
                "text": weekday.get_jp_date_str(date=date, with_day_of_week=True),
                "emoji": True,
            },
            "value": date.strftime("%Y-%m-%d"),
        }
        for date in activity_dates
    ]

    return {
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
                "label": {"type": "plain_text", "text": "今回は何時に設定しますか？"},
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
                "block_id": "commit-dates-block",
                "label": {
                    "type": "plain_text",
                    "text": "どの日に参加しますか？",
                },
                "element": {
                    "type": "checkboxes",
                    "action_id": "commit-dates-action",
                    "options": options,
                    "initial_options": options,
                },
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": "お休みの日があればチェックを外してください！",
                    },
                ],
            },
        ],
    }
