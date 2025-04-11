import json
import datetime

from fastapi import APIRouter, Request, Response
from zoneinfo import ZoneInfo

from ..repository.slack import slack_repository
from ..repository.firebase import (
    commitment_repository,
    point_repository,
    place_repository,
)
from ..models.point import Point, UserPoint, UserWinningTimes
from ..views import (
    cancel,
    commit_modal,
    help_command,
    commit_notification,
    absent_modal,
    absent_notification,
    commitments,
    status,
    results,
    leaderboard,
    places,
    mystats,
)
from ..constants import TARGET_CHANNEL_ID
from ..utils import weekday

router = APIRouter()

slack_client = slack_repository.client


@router.post("/slack/morning-command")
async def slack_morning_command(request: Request):
    form = await request.form()

    user_id = form["user_id"]
    command_text = form["text"]
    subcommand = command_text.split(" ")[0]

    print(f"Received morning command from {user_id}: `{form['text']}`.")

    if subcommand == "commit":
        next_activity_dates = weekday.get_next_coming_weekdays()
        response = slack_client.views_open(
            trigger_id=form["trigger_id"],
            view=commit_modal.modal_view(next_activity_dates),
        )
        print("Sent commit modal.")
        return Response(status_code=200)

    elif subcommand == "cancel":
        next_activity_dates = weekday.get_next_coming_weekdays()
        commitment_repository.disable_commits(
            user_id=user_id,
            dates=next_activity_dates,
        )
        slack_client.chat_postMessage(
            channel=TARGET_CHANNEL_ID,
            blocks=cancel.blocks(
                user_id=user_id,
                cancel_dates=next_activity_dates,
            ),
            text=commit_notification.text(
                user_id=user_id,
            ),
        )
        print("Sent cancel notification.")
        return Response(status_code=200)

    elif subcommand == "absent":
        today = datetime.datetime.now(ZoneInfo("Asia/Tokyo")).date()
        absent_date = today + datetime.timedelta(days=1)
        commits = commitment_repository.get_commit(
            date=absent_date,
        )
        for commit in commits:
            if commit.user_id == user_id:
                print("User has a commitment tomorrow.")
                break
        else:
            print("User doesn't have a commitment tomorrow.")
            return {
                "text": "明日の朝活には参加していません！\n（欠席連絡は前日のみ可能です）",
            }
        response = slack_client.views_open(
            trigger_id=form["trigger_id"],
            view=absent_modal.modal_view(absent_date),
        )
        print("Sent absent modal.")
        return Response(status_code=200)

    elif subcommand == "commitments":
        ongoing_or_coming_activity_dates = weekday.get_ongoing_or_coming_weekdays()
        user_commits = commitment_repository.get_user_commits(
            dates=ongoing_or_coming_activity_dates,
        )
        slack_client.chat_postMessage(
            channel=TARGET_CHANNEL_ID,
            blocks=commitments.blocks(
                user_commits=user_commits,
            ),
            text=commitments.text(),
        )
        print("Sent commitment list notification.")
        return Response(status_code=200)

    elif subcommand == "status":
        ongoing_or_last_activity_dates = weekday.get_ongoing_or_last_weekdays()
        points = point_repository.get_point(
            date=ongoing_or_last_activity_dates[0],
        )
        slack_client.chat_postMessage(
            channel=TARGET_CHANNEL_ID,
            blocks=status.blocks(
                points=points,
                dates=ongoing_or_last_activity_dates,
            ),
            text=status.text(),
        )
        print("Sent status notification.")
        return Response(status_code=200)
    elif subcommand == "results":
        today = datetime.datetime.now(ZoneInfo("Asia/Tokyo")).date()
        ongoing_or_last_activity_dates = weekday.get_ongoing_or_last_weekdays()
        if today < ongoing_or_last_activity_dates[-1]:
            return {
                "response_type": "in_channel",
                "text": "最終結果は朝活終了後に確認できます！:pray:",
            }
        points = point_repository.get_point(
            date=ongoing_or_last_activity_dates[0],
        )
        slack_client.chat_postMessage(
            channel=TARGET_CHANNEL_ID,
            blocks=results.blocks(
                points=points,
                dates=ongoing_or_last_activity_dates,
            ),
            text=results.text(),
        )
        print("Sent result notification.")
        return Response(status_code=200)
    elif subcommand == "leaderboard":
        user_winning_times: dict[str, UserWinningTimes] = {}
        points_of_weeks = point_repository.get_all_points_of_weeks()
        today = datetime.datetime.now(ZoneInfo("Asia/Tokyo")).date()

        ongoing_or_coming_activity_dates = weekday.get_ongoing_or_coming_weekdays()
        # 開催中の週を除くために検索
        for start_date_str, week_points in list(points_of_weeks.items()):
            start_date = week_points[0].start_date
            if start_date != ongoing_or_coming_activity_dates[0]:
                continue
            if today >= ongoing_or_coming_activity_dates[-1]:
                # 開催中でも最終日であれば残す
                continue
            # 開催中の週を除く
            points_of_weeks.pop(start_date_str)
            print(f"Removed ongoing week: {start_date}")

        # 週ごと
        for week_points in points_of_weeks.values():
            # この週のポイントランキング
            ranking = sorted(week_points, key=lambda x: x.point, reverse=True)
            # 優勝者のポイント
            first_place_point = ranking[0].point
            # 優勝者人数
            first_place_users_count = len(
                [point for point in ranking if point.point == first_place_point]
            )
            # ペナルティ合計
            total_penalty = sum([point.penalty for point in week_points]) * -1
            # 1人あたりの報酬ポイント
            reward_point = total_penalty / first_place_users_count
            for point in ranking:
                # 優勝回数と報酬をインクリメント
                if point.point < first_place_point:
                    break
                if point.user_id not in user_winning_times:
                    user_winning_times[point.user_id] = UserWinningTimes(
                        user_id=point.user_id,
                        user_name=point.user_name,
                        winning_times=1,
                        rewards=reward_point,
                    )
                else:
                    user_winning_times[point.user_id].winning_times += 1
                    user_winning_times[point.user_id].rewards += reward_point

        user_points = point_repository.get_all_user_points()

        all_user_commits = commitment_repository.get_all_user_commits()

        slack_client.chat_postMessage(
            channel=TARGET_CHANNEL_ID,
            blocks=leaderboard.blocks(
                user_winning_times=user_winning_times.values(),
                user_points=user_points,
                user_commits=all_user_commits,
            ),
            text=leaderboard.text(),
        )
        print("Sent leaderboard notification.")
        return Response(status_code=200)
    elif subcommand == "places":
        all_places = place_repository.get_enabled_places()
        slack_client.chat_postMessage(
            channel=TARGET_CHANNEL_ID,
            blocks=places.blocks(
                places=all_places,
            ),
            text=places.text(),
        )
        print("Sent places notification.")
        return Response(status_code=200)
    elif subcommand == "mystats":
        points_of_weeks = point_repository.get_all_points_of_weeks()
        today = datetime.datetime.now(ZoneInfo("Asia/Tokyo")).date()
        ongoing_or_coming_activity_dates = weekday.get_ongoing_or_coming_weekdays()
        # 開催中の週を除くために検索
        for start_date_str, week_points in list(points_of_weeks.items()):
            start_date = week_points[0].start_date
            if start_date != ongoing_or_coming_activity_dates[0]:
                continue
            if today >= ongoing_or_coming_activity_dates[-1]:
                # 開催中でも最終日であれば残す
                continue
            # 開催中の週を除く
            points_of_weeks.pop(start_date_str)
            print(f"Removed ongoing week: {start_date}")

        my_winning_times = 0
        my_joined_weeks_count = 0
        my_total_rewards = 0
        # 週ごと
        for week_points in points_of_weeks.values():
            # この週のポイントランキング
            ranking = sorted(week_points, key=lambda x: x.point, reverse=True)
            # 優勝者のポイント
            first_place_point = ranking[0].point
            # 優勝者人数
            first_place_users_count = len(
                [point for point in ranking if point.point == first_place_point]
            )
            # ペナルティ合計
            total_penalty = sum([point.penalty for point in week_points]) * -1
            # 1人あたりの報酬ポイント
            reward_point = total_penalty / first_place_users_count
            for point in ranking:
                # 自分のポイントでなければスキップ
                if point.user_id != user_id:
                    continue
                # 参加週数をインクリメント
                my_joined_weeks_count += 1
                # 優勝回数と報酬をインクリメント
                if point.point == first_place_point:
                    my_winning_times += 1
                    my_total_rewards += reward_point

        my_joined_days_count = 0
        all_user_commits = commitment_repository.get_all_user_commits()
        for user_commits in all_user_commits:
            if user_commits.user_id == user_id:
                my_joined_days_count = len(user_commits.dates)
                break

        user_points = point_repository.get_all_user_points()
        for my_points in user_points:
            if my_points.user_id == user_id:
                break

        slack_client.chat_postMessage(
            channel=TARGET_CHANNEL_ID,
            blocks=mystats.blocks(
                user_id=user_id,
                my_winning_times=my_winning_times,
                my_total_rewards=my_total_rewards,
                my_joined_weeks_count=my_joined_weeks_count,
                my_joined_days_count=my_joined_days_count,
                my_points=my_points,
            ),
            text=mystats.text(user_id=user_id),
        )
        print("Sent mystats notification.")
        return Response(status_code=200)
    elif subcommand == "help":
        return {
            "response_type": "in_channel",
            "blocks": help_command.blocks,
        }
    elif subcommand == "test":
        return {
            "text": "おはようございます！",
        }
    else:
        return {
            "response_type": "in_channel",
            "text": help_command.command_not_found_text,
        }


@router.post("/slack/interactivity")
async def slack_interactivity(request: Request):
    form = await request.form()
    payload = json.loads(form["payload"])

    user_id = payload["user"]["id"]
    user_name = payload["user"]["username"]
    modal_title = payload["view"]["title"]["text"]
    answers = payload["view"]["state"]["values"]
    blocks = payload["view"]["blocks"]

    print(f"Received submission of {modal_title} from {user_id} ({user_name}).")

    modal_title = payload["view"]["title"]["text"]
    if modal_title == "朝活の参加表明":
        commit_time = answers["commit-time-block"]["commit-time-action"][
            "selected_time"
        ]
        hour = int(commit_time.split(":")[0])
        minute = int(commit_time.split(":")[1])
        if hour < 5 or (hour == 12 and minute > 0) or hour > 12:
            return {
                "response_action": "errors",
                "errors": {
                    "commit-time-block": "朝活の時間は5時から12時までです！",
                },
            }

        commit_dates_block = next(
            block for block in blocks if block.get("block_id") == "commit-dates-block"
        )
        available_date_values = [
            option["value"] for option in commit_dates_block["element"]["options"]
        ]
        selected_date_values = [
            option["value"]
            for option in answers["commit-dates-block"]["commit-dates-action"][
                "selected_options"
            ]
        ]

        print(f"Commit time: {commit_time}")
        print(f"Available dates: {available_date_values}")
        print(f"Selected dates: {selected_date_values}")

        for date_value in available_date_values:
            date = datetime.datetime.strptime(date_value, "%Y-%m-%d").date()
            if date_value in selected_date_values:
                commitment_repository.put_commit(
                    user_id=user_id,
                    user_name=user_name,
                    time=commit_time,
                    date=date,
                    enabled=True,
                )
            else:
                commitment_repository.put_commit(
                    user_id=user_id,
                    user_name=user_name,
                    time=commit_time,
                    date=date,
                    enabled=False,
                )

        slack_client.chat_postMessage(
            channel=TARGET_CHANNEL_ID,
            blocks=commit_notification.blocks(
                user_id=user_id,
                commit_time=commit_time,
                commit_dates=selected_dates,
            ),
            text=commit_notification.text(
                user_id=user_id,
            ),
        )
        print("Sent commit notification.")
        return Response(status_code=200)

    elif modal_title == "欠席の連絡":
        absent_reason = answers["absent-reason-block"]["absent-reason-action"]["value"]
        today = datetime.datetime.now(ZoneInfo("Asia/Tokyo")).date()
        absent_date = today + datetime.timedelta(days=1)
        commitment_repository.disable_commit(
            user_id=user_id,
            date=absent_date,
        )
        slack_client.chat_postMessage(
            channel=TARGET_CHANNEL_ID,
            blocks=absent_notification.blocks(
                user_id=user_id,
                absent_reason=absent_reason,
            ),
            text=absent_notification.text(
                user_id=user_id,
            ),
        )
        print("Sent absent notification.")

        return Response(status_code=200)


@router.post("/slack/events")
async def slack_events(request: Request):
    request = await request.json()
    if request["type"] == "url_verification":
        return request["challenge"]

    body = await request.body()
    event = json.loads(body)["event"]

    if event["type"] == "app_home_opened":
        print(event)

        # Get channel members
        members_response = slack_client.conversations_members(
            channel=TARGET_CHANNEL_ID,
        )
        members = members_response["members"]

        if event["user"] not in members:
            return Response(status_code=200)
        else:
            slack_client.views_publish(
                user_id=event["user"],
                view={
                    "type": "home",
                    "blocks": [
                        {
                            "type": "section",
                            "text": {
                                "type": "plain_text",
                                "text": "このメッセージは朝活メンバーのみに表示されています！",
                                "emoji": True,
                            },
                        }
                    ],
                },
            )

    return Response(status_code=200)
