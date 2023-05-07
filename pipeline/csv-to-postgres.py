import os
import re
import pandas as pd 
from sqlalchemy import create_engine

csv_path = "/docker-entrypoint-initdb.d/listings.csv"
sql_path = "/docker-entrypoint-initdb.d/ddl.sql"

def locations_table(df):
    location=df.loc[:,[
        'neighbourhood',
        'latitude',
        'longitude',
        'neighborhood_overview',
    ]]
    location.rename(columns={
        'neighbourhood' : 'neighborhood'
    }, inplace=True)
    return location


def hosts_table(df):
    host=df.loc[:,[
        'host_id',
        'host_url',
        'host_name',
        'host_since',
        'host_location',
        'host_about',
        'host_response_rate',
        'host_acceptance_rate',
        'host_is_superhost',
        'host_neighbourhood',
        'host_listings_count',
        'host_total_listings_count',
        'host_verifications',
        'host_has_profile_pic',
        'host_identity_verified',
    ]]

    # remove 'host_' prefix from col names
    for col_i in range(1,len(host.columns)):
        if 'host_' in host.columns[col_i]:
            new = host.columns[col_i].replace('host_','')
            host.rename(columns={
                host.columns[col_i] : new
            }, inplace=True)
    
    # create lists of bools for verified email / phone
    email_bools, phone_bools = [], []
    for v in host['verifications']:
        email_bools.append(True) if "email" in v else email_bools.append(False)
        phone_bools.append(True) if "phone" in v else phone_bools.append(False)
    
    # insert columns in host df
    host.insert(14, 'email_verified', email_bools)
    host.insert(15, 'phone_verified', phone_bools)
    
    # delete verifications column
    del host['verifications']
    
    # change british spelling
    host.rename(columns={
        'neighbourhood' : 'neighborhood'
    }, inplace=True)

    i = 0
    for val in host.response_rate:
        if isinstance(val, str):
            host.loc[i,'acceptance_rate'] = float(val.strip('%'))
        i += 1

    j = 0
    for val in host.acceptance_rate:
        if isinstance(val, str):
            host.loc[j,'acceptance_rate'] = float(val.strip('%'))
        j += 1

    return host


def reviews_table(df):
    reviews=df.loc[:,[
        'number_of_reviews',
        'first_review',
        'last_review',
        'reviews_per_month',
        'review_scores_rating',
        'review_scores_accuracy',
        'review_scores_cleanliness',
        'review_scores_checkin',
        'review_scores_communication',
        'review_scores_location',
        'review_scores_value'
    ]]
    for col in reviews.columns:
        if "review_scores" in col:
            new = re.sub("review_scores_", "", col) + "_score"
            reviews.rename(columns = {
                col : new
            }, inplace=True)
    return reviews


def listings_table(df):
    listing=df.loc[:,[
        'listing_url',
        'name',
        'description',
        'property_type',
        'room_type',
        'accommodates',
        'bathrooms_text',
        'bedrooms',
        'beds',
        'amenities',
        'price',
        'minimum_nights',
        'maximum_nights',
    ]]
    i = 0
    for val in listing.price:
        if isinstance(val, str):
            if '$' in val:
                val = val.strip('$')
            if ',' in val:
                val = val.replace(',','')
            listing.loc[i, 'price'] = float(val)
        i += 1
    return listing




def load_data_to_postgres(): 
    # Read CSV file into a pandas DataFrame 
    df = pd.read_csv(csv_path)

    # Get transformed data
    locations = locations_table(df)
    hosts = hosts_table(df)
    reviews = reviews_table(df)
    listings = listings_table(df)

    # Define database connection settings 
    pg_user=os.environ.get("POSTGRES_USER")
    pg_password=os.environ.get("POSTGRES_PASSWORD")
    pg_host=os.environ.get("POSTGRES_HOST")
    pg_port=os.environ.get("CONTAINER_PORT")
    db_name=os.environ.get("POSTGRES_DB")
    
    # Create SQLAlchemy engine to connect to the PostgreSQL database 
    engine = create_engine(f'postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{db_name}')

    # Write DataFrame to a PostgreSQL table using the SQLAlchemy engine
    locations.to_sql(name='locations', con=engine, if_exists='replace', index=False)
    hosts.to_sql(name='hosts', con=engine, if_exists='replace', index=False)
    reviews.to_sql(name='reviews', con=engine, if_exists='replace',index=False)
    listings.to_sql(name='listings', con=engine, if_exists='replace',index=False)


if __name__ == '__main__':
    load_data_to_postgres()
