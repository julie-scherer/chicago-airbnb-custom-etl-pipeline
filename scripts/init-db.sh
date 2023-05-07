#!/bin/sh

# stop executing if any command fails or returns an error
set -e

# get the contents of the .env or example.env file into the script
if [ ! -f .env ]; then
    cp example.env .env
fi
set -a; . .env; set +a

# echo global variables in terminal
echo "DOCKER_CONTAINER_NAME=${DOCKER_CONTAINER_NAME}"
echo "POSTGRES_USER=${POSTGRES_USER}"
echo "POSTGRES_DB=${POSTGRES_DB}"

# run the psql command
psql \
    -v ON_ERROR_STOP=1 \
    -U "${POSTGRES_USER}" \
    -d "${POSTGRES_DB}" \
    -f /docker-entrypoint-initdb.d/ddl.sql

