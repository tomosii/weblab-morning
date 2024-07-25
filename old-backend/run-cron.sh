#!/bin/bash

call() {
    curl -sS "https://slack-morning-bot.vercel.app/cron"
}

while true; do
    call
    # Sleep for 5 minutes (300 seconds)
    sleep 300
done
