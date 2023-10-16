import os
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient

# Get tokens from environment variables
load_dotenv()

app = App(token=os.environ.get("SLACK_BOT_TOKEN"))


@app.command("/morning")
def handle_morning_command(ack, body, say, command, respond, client: WebClient):
    ack()
    sub_command = command["text"].split(" ")[0]

    if sub_command == "help":
        say(
            blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "お疲れ様です！\n/morning コマンドの使い方は以下の通りです！\n\n"
                        + "`/morning commit XX:XX`: 朝活の参加と時間を表明します。\n"
                        + "`/morning cancel`: 朝活への参加をキャンセルします。\n"
                        + "`/morning commitments`: 今週の朝活参加者一覧を表示します。\n"
                        + "`/morning summary`: 今週の朝活の結果を表示します。\n"
                        + "`/morning leaderboard`: 累計のランキングを表示します。\n"
                        + "`/morning help`: このヘルプを表示します。\n",
                    },
                }
            ],
            text="お疲れ様です！\n/morning コマンドの使い方は以下の通りです！",
        )
        return
    elif sub_command == "commit":
        say(f"<@{body['user_id']}>さんが朝活への参加を表明しました！ *10時00分*")
        return
    elif sub_command == "cancel":
        say(f"<@{body['user_id']}>さんが今週の朝活への参加をキャンセルしました！")
        return
    elif sub_command == "commitments":
        say(f"今週の朝活参加者は以下の通りです！")
        return
    elif sub_command == "summary":
        say(f"今週の結果は以下の通りです！")
        return
    else:
        client.chat_postEphemeral(
            channel=body["channel_id"],
            user=body["user_id"],
            text="コマンドが見つかりませんでした。 `/morning help` でヘルプを表示します。",
        )


@app.message("おはよう")
def message_hello(message: dict, say, client: WebClient):
    # Check if the message contains any files
    if message.get("files") is None:
        say(
            f"<@{message['user']}> 画像が添付されていないようです！ 写真を撮ってチェックインしましょう！:camera_with_flash:"
        )
        return

    # Record check-in
    say(f"<@{message['user']}>さん、おはようございます！:sunny: チェックインを記録しました。\n今日も一日頑張っていきましょう！")


if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
