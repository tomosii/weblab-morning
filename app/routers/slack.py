from fastapi import APIRouter, Request, Response
import json


from app.repository.slack.slack import slack_client
from app.views import commit_modal, help_command, commit_notification
from app.constants import channels

router = APIRouter()


@router.post("/slack/events")
def slack_events(request: Request):
    # URL verification
    return request["challenge"]


@router.post("/slack/morning-command")
async def slack_morning_command(request: Request):
    form = await request.form()
    print(form)

    user_id = form["user_id"]
    subcommand = form["text"].split(" ")[0]

    if subcommand == "commit":
        response = slack_client.views_open(
            trigger_id=form["trigger_id"],
            view=commit_modal.modal_view,
        )
        return Response(status_code=200)

    elif subcommand == "cancel":
        return {"response_type": "in_channel", "text": "この機能はまだ開発中です！:pray:"}
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
    answers = payload["view"]["state"]["values"]

    commit_time = answers["commit-time-block"]["commit-time-action"]["selected_time"]
    print(commit_time)
    hour = commit_time.split(":")[0]
    minute = commit_time.split(":")[1]

    commit_days_options = answers["commit-days-block"]["commit-days-action"][
        "selected_options"
    ]

    commit_days = [option["value"] for option in commit_days_options]
    commit_days_label = [option["text"]["text"] for option in commit_days_options]
    print(commit_days)

    slack_client.chat_postMessage(
        channel=channels.TARGET_CHANNEL_ID,
        blocks=commit_notification.blocks(
            user_id=payload["user"]["id"],
            commit_hours=hour,
            commit_minutes=minute,
            commit_days_labels=commit_days_label,
        ),
    )

    return Response(status_code=200)
