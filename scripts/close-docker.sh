#!/bin/sh

# stop executing if any command fails or returns an error
set -e

# get the contents of the .env or example.env file into the script
if [ -f .env ]; then
    . "$PWD/.env"
else
    . "$PWD/example.env"
fi

export DOCKER_CONTAINER="${DOCKER_CONTAINER}"
export DOCKER_IMAGE="${DOCKER_IMAGE}"

docker stop $DOCKER_CONTAINER \
&& docker rm $DOCKER_CONTAINER \
&& docker rmi $DOCKER_IMAGE


# optional, delete all images
# docker rmi -f $(docker images -aq)


# chmod +x scripts/close-docker.sh
# ./scripts/close-docker.sh
