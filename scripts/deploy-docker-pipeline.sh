#!/bin/sh

# stop executing if any command fails or returns an error
set -e

# get the contents of the .env or example.env file into the script
if [ ! -f .env ]; then
    cp example.env .env
fi
set -a; . .env; set +a

if docker ps | grep "${DOCKER_CONTAINER}" ; then
    echo "Stopping and removing container"
    docker stop $DOCKER_CONTAINER
    docker rm $DOCKER_CONTAINER
fi


# build the Docker image and start the container
docker build -t "$DOCKER_IMAGE" . --build-arg CONTAINER_PORT="$CONTAINER_PORT"

docker run --name "$DOCKER_CONTAINER" \
    --env-file .env \
    -e POSTGRES_PASSWORD="$POSTGRES_PASSWORD" \
    -e POSTGRES_DB="$POSTGRES_DB" \
    -d -p "$HOST_PORT:$CONTAINER_PORT" \
    "$DOCKER_IMAGE" 

# get the IP address of the container
DOCKER_IP=$(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' "$DOCKER_CONTAINER")
DOCKER_PORT=$(docker port $DOCKER_CONTAINER)
echo "Container $DOCKER_CONTAINER running! Forwarding connections from $DOCKER_PORT"


echo "Starting container... $(sleep 1 && docker start $DOCKER_CONTAINER)"
echo "Checking connection... $(sleep 1 && docker exec -it $DOCKER_CONTAINER pg_isready)"


# load data
docker exec chicago-airbnb-pgcontainer python3 /docker-entrypoint-initdb.d/csv-to-postgres.py


# (optional) now that the container is running, execute the psql command inside the container
# docker exec -it $DOCKER_CONTAINER \
#     psql -U $POSTGRES_USER -d $POSTGRES_DB



# chmod +x scripts/deploy-docker-pipeline.sh
# ./scripts/deploy-docker-pipeline.sh
