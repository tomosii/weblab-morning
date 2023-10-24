from fastapi import APIRouter, Request, Response
import json


from app.repository.slack import slack_repository
from app.repository.firebase import commitment_repository
from app.views import (
    cancel,
    commit_modal,
    help_command,
    commit_notification,
    absent_modal,
    absent_notification,
)
from app.constants import channels

router = APIRouter()

slack_client = slack_repository.client


@router.post("/slack/morning-command")
async def slack_morning_command(request: Request):
    form = await request.form()

    user_id = form["user_id"]
    command_text = form["text"]
    subcommand = command_text.split(" ")[0]

    print(f"Received morning command from {user_id}: {form['text']}")

    if subcommand == "commit":
        response = slack_client.views_open(
            trigger_id=form["trigger_id"],
            view=commit_modal.modal_view,
        )
        return Response(status_code=200)

    elif subcommand == "cancel":
        slack_client.chat_postMessage(
            channel=channels.DEV_CHANNEL_ID,
            blocks=cancel.blocks(
                user_id=user_id,
            ),
            text=commit_notification.text(
                user_id=user_id,
            ),
        )
        return Response(status_code=200)

    elif subcommand == "absent":
        response = slack_client.views_open(
            trigger_id=form["trigger_id"],
            view=absent_modal.modal_view,
        )
        return Response(status_code=200)

    elif subcommand == "commitments":
        return {"response_type": "in_channel", "text": "この機能はまだ開発中です！:pray:"}
    elif subcommand == "summary":
        return {"response_type": "in_channel", "text": "この機能はまだ開発中です！:pray:"}
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

    print(f"Received submission of {modal_title} from {user_id} ({user_name})")

    modal_title = payload["view"]["title"]["text"]
    if modal_title == "朝活の参加表明":
        commit_time = answers["commit-time-block"]["commit-time-action"][
            "selected_time"
        ]
        hour = commit_time.split(":")[0]
        minute = commit_time.split(":")[1]

        commit_days_options = answers["commit-days-block"]["commit-days-action"][
            "selected_options"
        ]

        commit_days = [option["value"] for option in commit_days_options]
        commit_days_label = [option["text"]["text"] for option in commit_days_options]

        print(f"Commit time: {commit_time}")
        print(f"Commit days: {commit_days}")

        slack_client.chat_postMessage(
            channel=channels.DEV_CHANNEL_ID,
            blocks=commit_notification.blocks(
                user_id=user_id,
                commit_hours=hour,
                commit_minutes=minute,
                commit_days_labels=commit_days_label,
            ),
            text=commit_notification.text(
                user_id=user_id,
            ),
        )

        commitment_repository.puts(
            user_id=user_id,
            user_name=user_name,
            time=commit_time,
            days=commit_days,
        )

        return Response(status_code=200)

    elif modal_title == "欠席の連絡":
        absent_reason = answers["absent-reason-block"]["absent-reason-action"]["value"]

        slack_client.chat_postMessage(
            channel=channels.DEV_CHANNEL_ID,
            blocks=absent_notification.blocks(
                user_id=user_id,
                reason=absent_reason,
            ),
            text=absent_notification.text(
                user_id=user_id,
            ),
        )

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
