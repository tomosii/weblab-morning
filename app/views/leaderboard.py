import datetime
from app.models.point import UserPoint, UserWinningTimes


def text():
    return f"今までの朝活を振り返ってみましょう！"


def blocks(
    user_winning_times: list[UserWinningTimes],
    user_points: list[UserPoint],
) -> list[dict]:
    # 勝利回数ランキング
    winning_times_ranking = sorted(
        user_winning_times,
        key=lambda x: x.winning_times,
        reverse=True,
    )
    print(f"Winning times ranking: {winning_times_ranking}")
    first_place_times: list[UserWinningTimes] = []
    second_place_times: list[UserWinningTimes] = []
    while len(winning_times_ranking) > 0:
        times = winning_times_ranking.pop(0)
        if len(first_place_times) == 0:
            first_place_times.append(times)
            continue
        elif times.winning_times == first_place_times[0].winning_times:
            first_place_times.append(times)
            continue
        elif len(second_place_times) == 0:
            second_place_times.append(times)
            continue
        elif times.winning_times == second_place_times[0].winning_times:
            second_place_times.append(times)
            continue
        else:
            break
    print(f"First place: {first_place_times}")
    print(f"Second place: {second_place_times}")

    # 累計ポイントランキング
    total_points_ranking = sorted(
        user_points,
        key=lambda x: x.total_point,
        reverse=True,
    )
    print(f"Total point ranking: {total_points_ranking}")
    first_place_points: list[UserPoint] = []
    second_place_points: list[UserPoint] = []
    while len(total_points_ranking) > 0:
        point = total_points_ranking.pop(0)
        if len(first_place_points) == 0:
            first_place_points.append(point)
            continue
        elif point.total_point == first_place_points[0].total_point:
            first_place_points.append(point)
            continue
        elif len(second_place_points) == 0:
            second_place_points.append(point)
            continue
        elif point.total_point == second_place_points[0].total_point:
            second_place_points.append(point)
            continue
        else:
            break
    print(f"First place: {first_place_points}")
    print(f"Second place: {second_place_points}")

    # 累計ペナルティランキング
    penalty_ranking = sorted(
        user_points,
        key=lambda x: x.total_penalty,
        reverse=True,
    )
    print(f"Total penalty ranking: {penalty_ranking}")
    first_place_penalty: list[UserPoint] = []
    second_place_penalty: list[UserPoint] = []
    while len(penalty_ranking) > 0:
        point = penalty_ranking.pop(0)
        if len(first_place_penalty) == 0:
            first_place_penalty.append(point)
            continue
        elif point.total_penalty == first_place_penalty[0].total_penalty:
            first_place_penalty.append(point)
            continue
        elif len(second_place_penalty) == 0:
            second_place_penalty.append(point)
            continue
        elif point.total_penalty == second_place_penalty[0].total_penalty:
            second_place_penalty.append(point)
            continue
        else:
            break
    print(f"First place: {first_place_penalty}")
    print(f"Second place: {second_place_penalty}")

    return [
        {
            "type": "section",
            "text": {
                "type": "plain_text",
                "text": "これまでの朝活を振り返ってみましょう！",
                "emoji": True,
            },
        },
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": ":crown: 勝利回数ランキング",
                "emoji": True,
            },
        },
        {"type": "divider"},
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f":first_place_medal: 1位   *{first_place_times[0].winning_times}勝*",
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
                                    "user_id": first_place_time.user_id,
                                }
                            ],
                        }
                        for first_place_time in first_place_times
                    ],
                }
            ],
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f":second_place_medal: 2位   *{second_place_times[0].winning_times}勝*",
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
                                    "user_id": second_place_time.user_id,
                                }
                            ],
                        }
                        for second_place_time in second_place_times
                    ],
                }
            ],
        },
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": ":gem: 累計ポイントランキング",
                "emoji": True,
            },
        },
        {"type": "divider"},
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f":first_place_medal: 1位   *{first_place_points[0].total_point}pt*",
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
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f":second_place_medal: 2位   *{second_place_points[0].total_point}pt*",
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
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": ":pleading_face: 累計ペナルティランキング",
                "emoji": True,
            },
        },
        {"type": "divider"},
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f":first_place_medal: 1位   *{first_place_penalty[0].total_penalty}pt*",
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
                        for first_place_point in first_place_penalty
                    ],
                }
            ],
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f":second_place_medal: 2位   *{second_place_penalty[0].total_penalty}pt*",
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
                        for second_place_point in second_place_penalty
                    ],
                }
            ],
        },
    ]
