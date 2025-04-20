import datetime

from utils import weekday


def modal_view(absent_date: datetime.date) -> dict:
    return {
        "type": "modal",
        "title": {"type": "plain_text", "text": "欠席の連絡"},
        "submit": {"type": "plain_text", "text": "確定"},
        "close": {"type": "plain_text", "text": "閉じる"},
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "text": f"{weekday.get_jp_date_str(date=absent_date, with_day_of_week=True)} の朝活を欠席しますか？",
                    "emoji": True,
                },
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": ":warning:  欠席連絡は前日の24時までです！",
                    }
                ],
            },
            {
                "type": "input",
                "block_id": "absent-reason-block",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "absent-reason-action",
                },
                "label": {
                    "type": "plain_text",
                    "text": "欠席の理由を教えてください :face_in_clouds:",
                },
            },
        ],
    }
