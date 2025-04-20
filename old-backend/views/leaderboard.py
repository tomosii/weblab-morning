import datetime
from models.point import UserPoint, UserWinningTimes
from models.commitment import UserCommitment


def text():
    return f"これまでの朝活を振り返ってみましょう！"


def blocks(
    user_winning_times: list[UserWinningTimes],
    user_points: list[UserPoint],
    user_commits: list[UserCommitment],
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
        reverse=False,
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

    # 累計報酬ランキング
    reward_ranking = sorted(
        user_winning_times,
        key=lambda x: x.rewards,
        reverse=True,
    )
    print(f"Total reward ranking: {reward_ranking}")
    first_place_rewards: list[UserWinningTimes] = []
    second_place_rewards: list[UserWinningTimes] = []
    while len(reward_ranking) > 0:
        times = reward_ranking.pop(0)
        if len(first_place_rewards) == 0:
            first_place_rewards.append(times)
            continue
        elif times.rewards == first_place_rewards[0].rewards:
            first_place_rewards.append(times)
            continue
        elif len(second_place_rewards) == 0:
            second_place_rewards.append(times)
            continue
        elif times.rewards == second_place_rewards[0].rewards:
            second_place_rewards.append(times)
            continue
        else:
            break
    print(f"First place: {first_place_rewards}")
    print(f"Second place: {second_place_rewards}")

    # 参加日数ランキング
    joined_days_ranking = sorted(
        user_commits,
        key=lambda x: len(x.dates),
        reverse=True,
    )
    print(f"Joined days ranking: {joined_days_ranking}")
    first_place_days: list[UserCommitment] = []
    second_place_days: list[UserCommitment] = []
    while len(joined_days_ranking) > 0:
        user_commit = joined_days_ranking.pop(0)
        if len(first_place_days) == 0:
            first_place_days.append(user_commit)
            continue
        elif len(user_commit.dates) == len(first_place_days[0].dates):
            first_place_days.append(user_commit)
            continue
        elif len(second_place_days) == 0:
            second_place_days.append(user_commit)
            continue
        elif len(user_commit.dates) == len(second_place_days[0].dates):
            second_place_days.append(user_commit)
            continue
        else:
            break
    print(f"First place: {first_place_days}")
    print(f"Second place: {second_place_days}")

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
                "text": ":crown: 通算勝利回数ランキング",
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
                "text": ":moneybag: 通算獲得報酬ランキング",
                "emoji": True,
            },
        },
        {"type": "divider"},
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f":first_place_medal: 1位   *{first_place_rewards[0].rewards}pt*",
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
                                    "user_id": first_place_reward.user_id,
                                }
                            ],
                        }
                        for first_place_reward in first_place_rewards
                    ],
                }
            ],
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f":second_place_medal: 2位   *{second_place_rewards[0].rewards}pt*",
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
                                    "user_id": second_place_reward.user_id,
                                }
                            ],
                        }
                        for second_place_reward in second_place_rewards
                    ],
                }
            ],
        },
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": ":pleading_face: 通算ペナルティランキング",
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
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": ":gem: 通算ポイントランキング",
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
                "text": ":date: 通算参加日数ランキング",
                "emoji": True,
            },
        },
        {"type": "divider"},
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f":first_place_medal: 1位   *{len(first_place_days[0].dates)}日*",
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
                                    "user_id": first_place_day.user_id,
                                }
                            ],
                        }
                        for first_place_day in first_place_days
                    ],
                }
            ],
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f":second_place_medal: 2位   *{len(second_place_days[0].dates)}日*",
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
                                    "user_id": second_place_day.user_id,
                                }
                            ],
                        }
                        for second_place_day in second_place_days
                    ],
                }
            ],
        },
    ]
