#!/bin/sh

# stop executing if any command fails or returns an error
set -e

# get the contents of the .env or example.env file into the script
if [ -f .env ]; then
    . .env
else
    . example.env
fi

export DOCKER_CONTAINER="${DOCKER_CONTAINER}"
export DOCKER_IMAGE="${DOCKER_IMAGE}"
export PG_DATABASE="${PG_DATABASE}"
export POSTGRES_USER="${POSTGRES_USER}"
export POSTGRES_PASSWORD="${POSTGRES_PASSWORD}"
export HOST_PORT="${HOST_PORT}"
export CONTAINER_PORT="${CONTAINER_PORT}"

echo "$DOCKER_CONTAINER"
echo "$DOCKER_IMAGE"

echo "$PG_DATABASE"
echo "$POSTGRES_USER"
echo "$POSTGRES_PASSWORD"

echo "$HOST_PORT"
echo "$CONTAINER_PORT"

# build the Docker image and start the container
docker build -t "$DOCKER_IMAGE" . --build-arg CONTAINER_PORT="$CONTAINER_PORT"

docker run --name "$DOCKER_CONTAINER" \
    -e POSTGRES_PASSWORD="$POSTGRES_PASSWORD" \
    -e POSTGRES_DB="$PG_DATABASE" \
    -d -p "$HOST_PORT:$CONTAINER_PORT" \
    "$DOCKER_IMAGE" 

# get the IP address of the container
DOCKER_IP=$(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' "$DOCKER_CONTAINER")
DOCKER_PORT=$(docker port $DOCKER_CONTAINER)
echo "Container $DOCKER_CONTAINER running! Forwarding connections from $DOCKER_PORT"


# docker logs $DOCKER_CONTAINER
echo "Starting container... $(sleep 1 && docker start $DOCKER_CONTAINER)"
echo "Checking connection... $(sleep 1 && docker exec -it $DOCKER_CONTAINER pg_isready)"


# (optional) now that the container is running, execute the psql command inside the container
docker exec -it $DOCKER_CONTAINER \
    psql -U $POSTGRES_USER -d $PG_DATABASE


# chmod +x scripts/run-docker.sh
# ./scripts/run-docker.sh
