from app.models.point import Point


def text():
    return f"現在の得点状況です！"


def blocks(points: list[Point]) -> list[dict]:
    # 合計ポイントで降順にソート
    ranking = sorted(
        points,
        key=lambda x: x.point,
        reverse=True,
    )
    print(f"Point ranking: {ranking}")

    first_place_points: list[Point] = []
    second_place_points: list[Point] = []
    while len(ranking) > 0:
        point = ranking.pop(0)
        if len(first_place_points) == 0:
            first_place_points.append(point)
            continue
        elif point.point == first_place_points[0].point:
            first_place_points.append(point)
            continue
        elif len(second_place_points) == 0:
            second_place_points.append(point)
            continue
        elif point.point == second_place_points[0].point:
            second_place_points.append(point)
            continue
    print(f"First place: {first_place_points}")
    print(f"Second place: {second_place_points}")

    penalty_points: list[Point] = []
    for point in points:
        if point.penalty < 0:
            penalty_points.append(point)
    print(f"Penalty points: {penalty_points}")

    _blocks = [
        {
            "type": "section",
            "text": {
                "type": "plain_text",
                "text": "得点状況です！",
                "emoji": True,
            },
        },
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": ":trophy: 現在のランキング",
                "emoji": True,
            },
        },
        {"type": "divider"},
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f":first_place_medal: 1位   *{first_place_points[0].point}pt*",
            },
        },
        {
            "type": "rich_text",
            "elements": [
                {
                    "type": "rich_text_list",
                    "style": "bullet",
                    "indent": 0,
                    "border": 0,
                    "elements": [
                        {
                            "type": "rich_text_section",
                            "elements": [
                                {
                                    "type": "user",
                                    "user_id": first_place_point.user_id,
                                }
                            ],
                        }
                        for first_place_point in first_place_points
                    ],
                }
            ],
        },
    ]

    if len(second_place_points) > 0:
        _blocks.extend(
            [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f":second_place_medal: 2位   *{second_place_points[0].point}pt*",
                    },
                },
                {
                    "type": "rich_text",
                    "elements": [
                        {
                            "type": "rich_text_list",
                            "style": "bullet",
                            "indent": 0,
                            "border": 0,
                            "elements": [
                                {
                                    "type": "rich_text_section",
                                    "elements": [
                                        {
                                            "type": "user",
                                            "user_id": second_place_point.user_id,
                                        }
                                    ],
                                }
                                for second_place_point in second_place_points
                            ],
                        }
                    ],
                },
            ]
        )

    _blocks.extend(
        [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": ":rotating_light: ペナルティ",
                    "emoji": True,
                },
            },
            {"type": "divider"},
        ]
    )

    if len(penalty_points) > 0:
        _blocks.append(
            {
                "type": "rich_text",
                "elements": [
                    {
                        "type": "rich_text_list",
                        "style": "bullet",
                        "indent": 0,
                        "border": 0,
                        "elements": [
                            {
                                "type": "rich_text_section",
                                "elements": [
                                    {
                                        "type": "user",
                                        "user_id": penalty_point.user_id,
                                    },
                                    {"type": "text", "text": "   "},
                                    {
                                        "type": "text",
                                        "text": f"{penalty_point.penalty}pt",
                                        "style": {"bold": True},
                                    },
                                ],
                            }
                            for penalty_point in penalty_points
                        ],
                    }
                ],
            },
        )
    else:
        _blocks.append(
            {
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "text": "今週はまだ誰も遅刻していません！",
                    "emoji": True,
                },
            },
        )
    return
