# Airbnb Chicago Listings PostgreSQL Database

## Project description

This project creates and deploys a PostgreSQL database in Docker and then uses Airflow to transform Airbnb listings data from Chicago, IL (data source: [Inside Airbnb](http://insideairbnb.com/chicago)) and load the processed data into the Postgres database running in Docker.

After the DAG is run, you can query the database using the `psql` command inside Docker (default container to exec is `chicago-airbnb-database-postgres-1`). The resulting database includes information about the listings, such as the property type, url, amenities, etc., as well as details about the location/neighborhood, host, and reviews from previous guests.

**Database schemas**

- **listings**: contains information about the Airbnb listings, such as the property type, room type, minimum and maximum nights, bedrooms, price, etc.
- **locations**: contains information about the location, including the Chicago neighborhood, latitude, longitude, and neighborhood overview.
- **hosts**: contains information about the hosts, such as their name and the number of listings they have.
- **reviews**: contains information about the reviews left by previous guests, such as the number of reviews, date, text of the review, etc.

The tables are linked together using foreign keys to allow for efficient queries and data retrieval.

## Getting started

### :information_source: Prerequisites 
* [Docker](https://docs.docker.com/get-docker/) installed
* Make installed (optional)

### :pencil: Instructions

1. First ensure that Docker is installed and running on your machine, and then navigate to the root directory of the project.

2. Create a copy of the `example.env` as `.env`. Note: Make will automatically create a copy if you don't have one when you run the `up` command.

    ```bash
    cp example.env .env
    ```


3. Start Airflow and run the DAG.
    
    ```bash
    make up

    # docker-compose up --remove-orphans --build -d
    ```

    &rarr; Now you should be able to access the Airflow UI at [http://localhost:8080/](http://localhost:8080/).

2. If everything worked correctly, you should now be able to access the PostgreSQL database by running this command in your terminal:

    ```bash
    make psql
    
    # source .env # need to export env variables first
    # docker exec -it ${PROJECT_NAME}-postgres-1 psql -U ${POSTGRES_USER} -d ${POSTGRES_DB}
    ```

3. When you are finished, clean up your Docker resources:

    ```
    make down
    
    # docker-compose down --volumes --rmi all
    ```
