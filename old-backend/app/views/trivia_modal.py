import datetime

from app.utils import weekday


def modal_view() -> dict:
    return {
        "type": "modal",
        "title": {"type": "plain_text", "text": "豆知識の追加"},
        "submit": {"type": "plain_text", "text": "確定"},
        "close": {"type": "plain_text", "text": "閉じる"},
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "text": "みんなに教えたい豆知識・雑学はありませんか？",
                    "emoji": True,
                },
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "plain_text",
                        "text": ":bulb: 最近知ったこと、誰かの恋愛話、研究に役立つTipsなど何でも！",
                        "emoji": True,
                    }
                ],
            },
            {
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "text": "朝活に遅刻せずに来た人にだけ表示されます！",
                    "emoji": True,
                },
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "plain_text",
                        "text": ":shushing_face: 誰が書いたのかは公開されません",
                        "emoji": True,
                    }
                ],
            },
            {
                "type": "input",
                "block_id": "trivia-create-block",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "trivia-create-action",
                },
                "label": {
                    "type": "plain_text",
                    "text": ":writing_hand: 豆知識を教えてください",
                    "emoji": True,
                },
            },
        ],
    }
