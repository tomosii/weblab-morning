#!/bin/bash

IMAGE_NAME="iiyama/slack-morning-bot"
CONTAINER_NAME="iiyama-slack-morning-bot-api"

CMD="uvicorn app.main:app --port 8080"

docker run -it --rm \
    --net=host \
    --env-file .env \
    --name $CONTAINER_NAME \
    $IMAGE_NAME \
    $CMD
