#!/bin/bash

IMAGE_NAME="iiyama/slack-morning-bot"
CONTAINER_NAME="iiyama-slack-morning-bot-ngrok"

CMD="ngrok http 8080"

docker run -it --rm \
    --net=host \
    --p 8080:8080 \
    --name $CONTAINER_NAME \
    $IMAGE_NAME