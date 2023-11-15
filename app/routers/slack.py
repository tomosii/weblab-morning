from fastapi import APIRouter, Request, Response
import json
import datetime

from zoneinfo import ZoneInfo
from app.repository.slack import slack_repository
from app.repository.firebase import (
    commitment_repository,
    point_repository,
    place_repository,
    trivia_repository,
)
from app.models.point import Point, UserPoint, UserWinningTimes
from app.views import (
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
    trivia_modal,
    trivia_notification,
)
from app.constants import TARGET_CHANNEL_ID
from app.utils import weekday

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
        for start_date in points_of_weeks.keys():
            if start_date != ongoing_or_coming_activity_dates[0]:
                continue
            if today >= ongoing_or_coming_activity_dates[-1]:
                # 開催中でも最終日であれば残す
                continue
            # 開催中の週を除く
            points_of_weeks.pop(start_date)
            print(f"Removed ongoing week: {start_date}")

        # 週ごと
        for week_points in points_of_weeks.values():
            # この週のポイントランキング
            ranking = sorted(week_points, key=lambda x: x.point, reverse=True)
            # 優勝者のポイント
            first_place_point = ranking[0].point
            for point in ranking:
                # 優勝回数をインクリメント
                if point.point < first_place_point:
                    break
                if point.user_id not in user_winning_times:
                    user_winning_times[point.user_id] = UserWinningTimes(
                        user_id=point.user_id,
                        user_name=point.user_name,
                        winning_times=1,
                    )
                else:
                    user_winning_times[point.user_id].winning_times += 1

        user_points = point_repository.get_all_user_points()

        slack_client.chat_postMessage(
            channel=TARGET_CHANNEL_ID,
            blocks=leaderboard.blocks(
                user_winning_times=user_winning_times.values(),
                user_points=user_points,
            ),
            text=leaderboard.text(),
        )
        print("Sent leaderboard notification.")
        return Response(status_code=200)
    elif subcommand == "places":
        all_places = place_repository.get_places()
        slack_client.chat_postMessage(
            channel=TARGET_CHANNEL_ID,
            blocks=places.blocks(
                places=all_places,
            ),
            text=places.text(),
        )
        print("Sent places notification.")
        return Response(status_code=200)
    elif subcommand == "trivia":
        response = slack_client.views_open(
            trigger_id=form["trigger_id"],
            view=trivia_modal.modal_view(),
        )
        print("Sent trivia modal.")
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

    print(f"Received submission of {modal_title} from {user_id} ({user_name}).")

    modal_title = payload["view"]["title"]["text"]
    if modal_title == "朝活の参加表明":
        commit_time = answers["commit-time-block"]["commit-time-action"][
            "selected_time"
        ]
        commit_dates_options = answers["commit-dates-block"]["commit-dates-action"][
            "selected_options"
        ]
        commit_dates = [
            datetime.datetime.strptime(option["value"], "%Y-%m-%d").date()
            for option in commit_dates_options
        ]

        print(f"Commit time: {commit_time}")
        print(f"Commit dates: {commit_dates}")

        commitment_repository.put_commits(
            user_id=user_id,
            user_name=user_name,
            time=commit_time,
            dates=commit_dates,
        )

        slack_client.chat_postMessage(
            channel=TARGET_CHANNEL_ID,
            blocks=commit_notification.blocks(
                user_id=user_id,
                commit_time=commit_time,
                commit_dates=commit_dates,
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
    elif modal_title == "豆知識の追加":
        trivia_text = answers["trivia-create-block"]["trivia-create-action"]["value"]
        created_at = datetime.datetime.now(ZoneInfo("Asia/Tokyo"))
        trivia_repository.put_trivia(
            user_id=user_id,
            user_name=user_name,
            trivia_text=trivia_text,
            created_at=created_at,
        )
        slack_client.chat_postMessage(
            channel=TARGET_CHANNEL_ID,
            blocks=trivia_notification.blocks(),
            text=trivia_notification.text(),
        )
        print("Sent trivia notification.")
        return {
            "blocks": trivia_notification.ephemeral_blocks(trivia_text),
        }


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
