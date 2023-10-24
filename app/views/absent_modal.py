modal_view = {
    "type": "modal",
    "title": {"type": "plain_text", "text": "欠席の連絡"},
    "submit": {"type": "plain_text", "text": "確定"},
    "close": {"type": "plain_text", "text": "閉じる"},
    "blocks": [
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
