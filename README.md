# Airbnb Chicago Listings PostgreSQL Database


## Project description

This repository creates a PostgreSQL database from the Inside Airbnb listings data for Chicago, IL [available here](http://insideairbnb.com/get-the-data/). The database includes information about the listings, such as the property type, url, amenities, etc., as well as details about the location/neighborhood, host, and reviews from previous guests.

&rarr; Note that this repository is currently under development. The database has been configured to run in Docker and the necessary tables have been created. However, the data has not been inserted yet. Updates coming soon :smile:

**Data source:**

The Airbnb listings data for Chicago, IL was obtained from the [Inside Airbnb](http://insideairbnb.com/chicago) website. The data includes listings that were active as of December 2022.

**Database design**

The database has been designed with the following tables:

- listings: contains information about the Airbnb listings, such as the property type, room type, minimum and maximum nights, bedrooms, price, etc.
- location: contains information about the location, including the Chicago neighborhood, latitude, longitude, and neighborhood overview.
- hosts: contains information about the hosts, such as their name and the number of listings they have.
- reviews: contains information about the reviews left by previous guests, such as the number of reviews, date, text of the review, etc.

The tables are linked together using foreign keys to allow for efficient queries and data retrieval.

## Getting started

### :information_source: Prerequisites 
* [Docker](https://docs.docker.com/get-docker/) installed
* Make installed (optional)
* Database client installed (optional)

The instructions below assume you have an `.env` file in the root directory with the following environment variables defined. Otherwise, it will use the `example.env` file.

### :pencil: Instructions

1. Start the Docker daemon, open a terminal window, and navigate to the root directory of the forked repository

2. Run the following commands to make the script file executable and run the script:
    
    ```
    chmod +x scripts/run-docker.sh
	./scripts/run-docker.sh

    # or, run this command if you have Make:
    # make up
    ```

    &rarr; The `run-docker.sh` script will build a Docker image using the Postgres image on [Docker Hub](https://hub.docker.com/_/postgres), start a new container from the image, and output the IP address and port number of the container. You can then use the IP address and port number to connect to the Postgres database in the container.

    &rarr; This will create the `host`, `listing`, `location`, and `reviews` tables in the Postgres database, which I named `airbnb` in the example.env file but you are welcome to change.

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

    * **Host**: The IP address of the Docker container running the PostgreSQL instance. You can find this printed in the terminal from when you ran the `run-docker.sh` script. It will most likely be `0.0.0.0` or `localhost`.

    * **Port**: The port that you exposed when you started the container. This should be the same as the `$CONTAINER_PORT` variable in your `.env` or `example.env` file. Default port is `5431:5432`.

    * **Database**: The name of the database that you want to connect to. This should be the same as the `$POSTGRES_DB` variable in your `.env` or `example.env` file. Default is `airbnb`.

    * **Username**: The username that you want to use to connect to the database. This should be the same as the `$POSTGRES_USER` variable in your `.env` or `example.env` file. Default is `postgres`.

    * **Password**: The password that you want to use to connect to the database. This should be the same as the `$POSTGRES_PASSWORD` variable in your `.env` or `example.env` file. Default is `postgres`.

    Once you have filled in these properties, click "Test Connection" to make sure that client can connect to the database.

3. If the test connection is successful, click "Finish" or "Save" to save the connection. You should now be able to use the database client to manage your PostgreSQL database running in Docker.
