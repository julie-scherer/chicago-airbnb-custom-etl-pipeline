FROM postgres:latest

ARG CONTAINER_PORT=${CONTAINER_PORT}

# The /docker-entrypoint-initdb.d/ directory is used by the official
# Postgres Docker image as a location for scripts and data files
# that need to be executed or loaded during database initialization.

COPY data/listings.csv /docker-entrypoint-initdb.d/listings.csv
COPY sql/ddl.sql /docker-entrypoint-initdb.d/ddl.sql


COPY example.env /docker-entrypoint-initdb.d/
COPY scripts/run-postgres.sh /docker-entrypoint-initdb.d/
RUN chmod +x /docker-entrypoint-initdb.d/run-postgres.sh

CMD ["postgres"]

EXPOSE $CONTAINER_PORT