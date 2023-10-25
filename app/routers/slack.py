from fastapi import APIRouter, Request, Response
import json
import datetime


from app.repository.slack import slack_repository
from app.repository.firebase import commitment_repository
from app.views import (
    cancel,
    commit_modal,
    help_command,
    commit_notification,
    absent_modal,
    absent_notification,
    commitments,
    summary,
)
from app.constants import channels
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
            channel=channels.DEV_CHANNEL_ID,
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
        absent_date = datetime.date.today() + datetime.timedelta(days=1)
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
            channel=channels.DEV_CHANNEL_ID,
            blocks=commitments.blocks(
                user_commits=user_commits,
            ),
            text=commitments.text(),
        )
        print("Sent commitment list notification.")
        return Response(status_code=200)

    elif subcommand == "summary":
        ongoing_or_last_activity_dates = weekday.get_ongoing_or_last_weekdays()
        user_commits = commitment_repository.get_user_commits(
            dates=ongoing_or_last_activity_dates,
        )
        slack_client.chat_postMessage(
            channel=channels.DEV_CHANNEL_ID,
            blocks=summary.blocks(
                winner_id="",
                user_points=[],
            ),
            text=summary.text(),
        )

        print("Sent summary notification.")
        return Response(status_code=200)
    elif subcommand == "leaderboard":
        return {"response_type": "in_channel", "text": "この機能はまだ開発中です！:pray:"}
    elif subcommand == "help":
        return {
            "response_type": "in_channel",
            "blocks": help_command.blocks,
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
            channel=channels.DEV_CHANNEL_ID,
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
        absent_date = datetime.date.today() + datetime.timedelta(days=1)

        commitment_repository.disable_commit(
            user_id=user_id,
            date=absent_date,
        )

        slack_client.chat_postMessage(
            channel=channels.DEV_CHANNEL_ID,
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
            channel=channels.DEV_CHANNEL_ID
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
