#!/bin/bash

IMAGE_NAME="ngrok/ngrok"
CONTAINER_NAME="iiyama-slack-morning-bot-ngrok"

CMD="http 8080"

docker run -it --rm \
    --net=host \
    --name $CONTAINER_NAME \
    $IMAGE_NAME \
    $CMD
