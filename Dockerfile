FROM postgres:latest

ARG CONTAINER_PORT=${CONTAINER_PORT}

# The /docker-entrypoint-initdb.d/ directory is used by the official
# Postgres Docker image as a location for scripts and data files
# that need to be executed or loaded during database initialization.

COPY data/listings.csv /docker-entrypoint-initdb.d/listings.csv
COPY sql/ddl.sql /docker-entrypoint-initdb.d/ddl.sql
COPY pipeline/csv-to-postgres.py /docker-entrypoint-initdb.d/

COPY scripts/init-db.sh /docker-entrypoint-initdb.d/

RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    pip3 install --no-cache-dir pandas sqlalchemy psycopg2-binary

RUN chmod +x /docker-entrypoint-initdb.d/csv-to-postgres.py
RUN chmod +x /docker-entrypoint-initdb.d/init-db.sh

CMD ["postgres"]

EXPOSE $CONTAINER_PORT