#!/bin/bash

IMAGE_NAME="iiyama/slack-morning-bot"
CONTAINER_NAME="iiyama-slack-morning-bot-api"

CMD="uvicorn app.main:app --reload"

docker run -it --rm \
    --net=host \
    --p 8080:8080 \
    --name $CONTAINER_NAME \
    $IMAGE_NAME