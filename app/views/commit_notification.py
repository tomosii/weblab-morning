import datetime

from app.utils import weekday


def text(user_id: str):
    return f"<@{user_id}> さんが朝活への参加を宣言しました！:fire:"


def blocks(user_id: str, commit_time: str, commit_dates: list[datetime.date]):
    hour = commit_time.split(":")[0]
    minute = commit_time.split(":")[1]
    dates_with_commas = ",  ".join(
        [
            weekday.get_jp_date_str(date=date, with_day_of_week=False)
            for date in commit_dates
        ]
    )

    return [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"<@{user_id}> さんが朝活の参加を宣言しました！:fire:",
            },
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f":clock10:  *{hour}時{minute}分*",
            },
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": dates_with_commas,
                },
            ],
        },
        # {
        #     "type": "rich_text",
        #     "elements": [
        #         {
        #             "type": "rich_text_list",
        #             "style": "bullet",
        #             "indent": 0,
        #             "border": 1,
        #             "elements": [
        #                 {
        #                     "type": "rich_text_section",
        #                     "elements": [
        #                         {
        #                             "type": "text",
        #                             "text": f"{day}",
        #                             "style": {"code": True},
        #                         },
        #                     ],
        #                 }
        #                 for day in commit_days_labels
        #             ],
        #         },
        #     ],
        # },
    ]
