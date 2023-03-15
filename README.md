## Airbnb Chicago Listings PostgreSQL Database


#### Project description: 

This repository creates a PostgreSQL database from the Inside Airbnb listings data for Chicago, IL [available here](http://insideairbnb.com/get-the-data/). The database includes information about the listings, such as the property type, url, amenities, etc., as well as details about the location/neighborhood, host, and reviews from previous guests.

#### Data source: 
The Airbnb listings data for Chicago, IL was obtained from the [Inside Airbnb](http://insideairbnb.com/chicago) website. The data includes listings that were active as of December 2022.


#### Database design: 
The database has been designed with the following tables:

- listings: contains information about the Airbnb listings, such as the property type, room type, minimum and maximum nights, bedrooms, price, etc.
- location: contains information about the location, including the Chicago neighborhood, latitude, longitude, and neighborhood overview.
- hosts: contains information about the hosts, such as their name and the number of listings they have.
- reviews: contains information about the reviews left by previous guests, such as the number of reviews, date, text of the review, etc.

The tables are linked together using foreign keys to allow for efficient queries and data retrieval.