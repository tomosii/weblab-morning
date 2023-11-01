import datetime

from app.utils import weekday
from app.models.point import Point


def text():
    return f"今週の朝活勝者の発表です！"


def blocks(points: list[Point]) -> list[dict]:
    # 合計ポイントで降順にソート
    ranking = sorted(points, key=lambda x: x.point, reverse=True)
    print(f"Point ranking: {ranking}")

    first_place_points: list[Point] = []
    while len(ranking) > 0:
        point = ranking.pop(0)
        if len(first_place_points) == 0:
            first_place_points.append(point)
            continue
        elif point.point == first_place_points[0].point:
            first_place_points.append(point)
            continue

    print(f"First place: {first_place_points}")

    winners_ids = [f"*<@{point.user_id}>* さん" for point in first_place_points]
    winner_text = "、".join(winners_ids)

    _blocks = [
        {
            "type": "section",
            "text": {
                "type": "plain_text",
                "text": "1週間お疲れ様でした！",
                "emoji": True,
            },
        },
        {
            "type": "section",
            "text": {
                "type": "plain_text",
                "text": "今週の朝活の勝者は ....",
                "emoji": True,
            },
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f":trophy: {winner_text}です！！:tada:",
            },
        },
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": ":star: 結果",
                "emoji": True,
            },
        },
        {"type": "divider"},
        {
            "type": "section",
            "fields": [
                {"type": "mrkdwn", "text": "<@U04QANYLPK6>"},
                {"type": "mrkdwn", "text": "*`2pt`*"},
            ],
        },
        {
            "type": "section",
            "fields": [
                {"type": "mrkdwn", "text": "<@U039S8P0B9T>"},
                {"type": "mrkdwn", "text": "*`2pt`*  (-2pt)"},
            ],
        },
        {
            "type": "section",
            "fields": [
                {"type": "mrkdwn", "text": "<@U04Q5BG479T>"},
                {"type": "mrkdwn", "text": "*`2pt`*"},
            ],
        },
    ]

    for point in points:
        point_text = f"*`{point.point}pt`*"
        if point.penalty < 0:
            point_text += f"  ({point.penalty}pt)"

        _blocks.append(
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"<@{point.user_id}>"},
                    {"type": "mrkdwn", "text": point_text},
                ],
            }
        )

    return _blocks
