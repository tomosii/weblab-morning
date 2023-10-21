from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response
import json
import firebase_admin
from firebase_admin import firestore
import os
from slack_sdk import WebClient

load_dotenv()

app = FastAPI()

firebase_app = firebase_admin.initialize_app()
db = firestore.client()

slack_client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))

# CHANNEL_ID = "C060S2Z6E15"
CHANNEL_ID = "C0616PTQ6AF"


@app.get("/")
def read_root():
    places = db.collection("place").stream()
    return {"places": [place.to_dict() for place in places]}


# URL verification
@app.post("/slack/events")
def slack_events(request: dict):
    return request["challenge"]


# Morning command
@app.post("/slack/morning-command")
async def slack_morning_command(request: Request):
    form = await request.form()
    print(form)

    user_id = form["user_id"]

    subcommand = form["text"].split(" ")[0]

    if subcommand == "commit":
        response = slack_client.views_open(
            trigger_id=form["trigger_id"],
            view={
                "type": "modal",
                "title": {"type": "plain_text", "text": "朝活の参加表明"},
                "submit": {"type": "plain_text", "text": "確定"},
                "close": {"type": "plain_text", "text": "閉じる"},
                "blocks": [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": ":clock10:  時間の設定",
                            "emoji": True,
                        },
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "plain_text",
                            "text": "数字を直接入力すると細かい時間指定ができます！",
                            "emoji": True,
                        },
                    },
                    {
                        "type": "input",
                        "block_id": "commit-time-block",
                        "element": {
                            "type": "timepicker",
                            "initial_time": "10:00",
                            "action_id": "commit-time-action",
                        },
                        "label": {"type": "plain_text", "text": "今週は何時に設定しますか？"},
                    },
                    {"type": "divider"},
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": ":date:  曜日の設定",
                            "emoji": True,
                        },
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "plain_text",
                            "text": "お休みの日があればチェックを外してください！",
                            "emoji": True,
                        },
                    },
                    {
                        "type": "input",
                        "block_id": "commit-days-block",
                        "label": {
                            "type": "plain_text",
                            "text": "どの日に参加しますか？",
                        },
                        "element": {
                            "type": "checkboxes",
                            "action_id": "commit-days-action",
                            "options": [
                                {
                                    "text": {
                                        "type": "plain_text",
                                        "text": "10/16 (月)",
                                        "emoji": True,
                                    },
                                    "value": "2023-10-16",
                                },
                                {
                                    "text": {
                                        "type": "plain_text",
                                        "text": "10/17 (火)",
                                        "emoji": True,
                                    },
                                    "value": "2023-10-17",
                                },
                                {
                                    "text": {
                                        "type": "plain_text",
                                        "text": "10/18 (水)",
                                        "emoji": True,
                                    },
                                    "value": "2023-10-18",
                                },
                                {
                                    "text": {
                                        "type": "plain_text",
                                        "text": "10/19 (木)",
                                        "emoji": True,
                                    },
                                    "value": "2023-10-19",
                                },
                                {
                                    "text": {
                                        "type": "plain_text",
                                        "text": "10/20 (金)",
                                        "emoji": True,
                                    },
                                    "value": "2023-10-20",
                                },
                            ],
                            "initial_options": [
                                {
                                    "text": {
                                        "type": "plain_text",
                                        "text": "10/16 (月)",
                                    },
                                    "value": "2023-10-16",
                                },
                                {
                                    "text": {
                                        "type": "plain_text",
                                        "text": "10/17 (火)",
                                    },
                                    "value": "2023-10-17",
                                },
                                {
                                    "text": {
                                        "type": "plain_text",
                                        "text": "10/18 (水)",
                                    },
                                    "value": "2023-10-18",
                                },
                                {
                                    "text": {
                                        "type": "plain_text",
                                        "text": "10/19 (木)",
                                    },
                                    "value": "2023-10-19",
                                },
                                {
                                    "text": {
                                        "type": "plain_text",
                                        "text": "10/20 (金)",
                                    },
                                    "value": "2023-10-20",
                                },
                            ],
                        },
                    },
                ],
            },
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
            "blocks": [
                {
                    "type": "rich_text",
                    "elements": [
                        {
                            "type": "rich_text_section",
                            "elements": [
                                {
                                    "type": "text",
                                    "text": "/morning コマンドの使い方は以下の通りです！\n",
                                },
                            ],
                        },
                        {
                            "type": "rich_text_list",
                            "style": "bullet",
                            "elements": [
                                {
                                    "type": "rich_text_section",
                                    "elements": [
                                        {
                                            "type": "text",
                                            "text": "/morning commit",
                                            "style": {"code": True},
                                        },
                                        {
                                            "type": "text",
                                            "text": ": 朝活の参加と時間を表明します。",
                                        },
                                    ],
                                },
                                {
                                    "type": "rich_text_section",
                                    "elements": [
                                        {
                                            "type": "text",
                                            "text": "/morning cancel",
                                            "style": {"code": True},
                                        },
                                        {
                                            "type": "text",
                                            "text": ": 朝活への参加をキャンセルします。",
                                        },
                                    ],
                                },
                                {
                                    "type": "rich_text_section",
                                    "elements": [
                                        {
                                            "type": "text",
                                            "text": "/morning commitments",
                                            "style": {"code": True},
                                        },
                                        {
                                            "type": "text",
                                            "text": ": 今週の朝活参加者一覧を表示します。",
                                        },
                                    ],
                                },
                                {
                                    "type": "rich_text_section",
                                    "elements": [
                                        {
                                            "type": "text",
                                            "text": "/morning summary",
                                            "style": {"code": True},
                                        },
                                        {
                                            "type": "text",
                                            "text": ": 今週の朝活の結果を表示します。",
                                        },
                                    ],
                                },
                                {
                                    "type": "rich_text_section",
                                    "elements": [
                                        {
                                            "type": "text",
                                            "text": "/morning leaderboard",
                                            "style": {"code": True},
                                        },
                                        {
                                            "type": "text",
                                            "text": ": 累計のランキングを表示します。",
                                        },
                                    ],
                                },
                                {
                                    "type": "rich_text_section",
                                    "elements": [
                                        {
                                            "type": "text",
                                            "text": "/morning help",
                                            "style": {"code": True},
                                        },
                                        {
                                            "type": "text",
                                            "text": ": このヘルプを表示します。",
                                        },
                                    ],
                                },
                            ],
                        },
                    ],
                },
            ],
        }

    else:
        return {
            "response_type": "in_channel",
            "text": "コマンドが見つかりませんでした。 `/morning help` でヘルプを表示します。",
        }


@app.post("/slack/interactivity")
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
        channel=CHANNEL_ID,
        blocks=[
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"<@{payload['user']['id']}> さんが朝活への参加を表明しました！",
                },
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*{hour}時{minute}分*",
                },
            },
            {
                "type": "rich_text",
                "elements": [
                    {
                        "type": "rich_text_list",
                        "style": "bullet",
                        "indent": 0,
                        "border": 1,
                        "elements": [
                            {
                                "type": "rich_text_section",
                                "elements": [
                                    {
                                        "type": "text",
                                        "text": f"{day}",
                                    },
                                ],
                            }
                            for day in commit_days_label
                        ],
                    },
                ],
            },
        ],
    )

    return Response(status_code=200)
