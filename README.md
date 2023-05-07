# Airbnb Chicago Listings PostgreSQL Database


## Project description

This project creates and deploys a PostgreSQL database in Docker, processes Airbnb listings data from Chicago, IL (data source: [Inside Airbnb](http://insideairbnb.com/chicago)), and then loads the transformed data into the Postgres database running in Docker.

TL;DR The database definition script `sql/ddl.sql` and the data insertion script `csv-to-postgres.py` are automatically executed when the `deploy-docker-pipeline.sh` script is run.

The resulting database includes information about the listings, such as the property type, url, amenities, etc., as well as details about the location/neighborhood, host, and reviews from previous guests.

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
* Database client installed (optional)

The instructions below assume you have an `.env` file in the root directory with the following environment variables defined. Otherwise, it will use the `example.env` file.

### :pencil: Instructions

1. To run the pipeline, ensure that Docker is installed and running on your machine, and then navigate to the root directory of the project in the terminal and run the following command:
    
    ```
    chmod +x scripts/deploy-docker-pipeline.sh
    ./scripts/deploy-docker-pipeline.sh

    # or, run this command if you have Make:
    # make up
    ```

    The `deploy-docker-pipeline.sh` script will build the `chicago-airbnb-pgimage` Docker image using the Postgres image on [Docker Hub](https://hub.docker.com/_/postgres), start the `chicago-airbnb-pgcontainer` Docker container, and output the IP address and port of the container, which you can use to connect to the database. The bash script creates four tables - `hosts`, `listings`, `locations`, and `reviews` tables - in the `airbnb` database and then runs the `csv-to-postgres.py` script to insert the csv data into the Postgres database.

2. Once the pipeline has finished running, you should be able to connect to the PostgreSQL database using your preferred client and view the data in the tables.

3. When you are finished with the Postgres container, you can clean up Docker with the following commands:

    ```
    chmod +x scripts/close-docker.sh
	./scripts/close-docker.sh

    # alternatively, if you have Make:
    # make down
    ```

    &rarr; This will stop and remove the Docker container and Docker image.

### :electric_plug: Connecting to a database client

To connect a database client to the Postgres instance running in Docker, you can follow these steps:

1. Open the client and create a new PostgreSQL connection.

2. In the "Connection Settings" window, set the following properties:

    * **Host**: The IP address of the Docker container running the PostgreSQL instance. This should be the same as the `$POSTGRES_HOST` variable in your `.env` or `example.env` file. Default port is `localhost` or `0.0.0.0`.

    * **Port**: The port that you exposed when you started the container. This should be the same as the `$CONTAINER_PORT` variable in your `.env` or `example.env` file. Default port is `5431:5432`.

    * **Database**: The name of the database that you want to connect to. This should be the same as the `$POSTGRES_DB` variable in your `.env` or `example.env` file. Default is `airbnb`.

    * **Username**: The username that you want to use to connect to the database. This should be the same as the `$POSTGRES_USER` variable in your `.env` or `example.env` file. Default is `postgres`.

    * **Password**: The password that you want to use to connect to the database. This should be the same as the `$POSTGRES_PASSWORD` variable in your `.env` or `example.env` file. Default is `postgres`.

    Once you have filled in these properties, click "Test Connection" to make sure that client can connect to the database.

3. If the test connection is successful, click "Finish" or "Save" to save the connection. You should now be able to use the database client to manage your PostgreSQL database running in Docker.
