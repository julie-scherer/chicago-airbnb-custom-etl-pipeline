import os
import re
import pandas as pd 
from sqlalchemy import create_engine

from airflow import DAG
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta

default_args = { 
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 5, 5), 
    'retries': 2,
    'retry_delay': timedelta(seconds=30)

}

dag = DAG('load_csv_to_postgres', default_args=default_args, schedule_interval='@once')


csv_path = "/opt/airflow/data/listings.csv"
sql_path = "/opt/airflow/data/ddl.sql"


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
    POSTGRES_USER=os.environ.get("POSTGRES_USER")
    POSTGRES_PASSWORD=os.environ.get("POSTGRES_PASSWORD")
    POSTGRES_HOST=os.environ.get("POSTGRES_HOST")
    POSTGRES_PORT=os.environ.get("POSTGRES_PORT")
    POSTGRES_DB=os.environ.get("POSTGRES_DB")
    
    # Create SQLAlchemy engine to connect to the PostgreSQL database 
    engine = create_engine(f'postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}')

    # Write DataFrame to a PostgreSQL table using the SQLAlchemy engine
    locations.to_sql(name='locations', con=engine, if_exists='replace', index=False)
    hosts.to_sql(name='hosts', con=engine, if_exists='replace', index=False)
    reviews.to_sql(name='reviews', con=engine, if_exists='replace',index=False)
    listings.to_sql(name='listings', con=engine, if_exists='replace',index=False)




# ** Using PostgresOperator **
create_table = PostgresOperator(
    task_id='create_tables',
    postgres_conn_id='postgres_connection',
    sql="""
    CREATE TABLE IF NOT EXISTS location (
        id SERIAL PRIMARY KEY
        ,neighborhood VARCHAR
        ,latitude NUMERIC(6,4)
        ,longitude NUMERIC(6,4)
        ,neighborhood_overview TEXT   
    );
    CREATE TABLE IF NOT EXISTS host (
        id SERIAL PRIMARY KEY
        ,host_id INT
        ,url VARCHAR
        ,name VARCHAR
        ,since DATE
        ,location VARCHAR
        ,about TEXT
        ,response_rate INT CHECK (response_rate <= 100)
        ,acceptance_rate INT CHECK (acceptance_rate <= 100)
        ,is_superhost BOOLEAN
        ,neighborhood VARCHAR
        ,listings_count INT
        ,total_listings_count INT
        ,email_verified BOOLEAN
        ,phone_verified BOOLEAN
        ,has_profile_pic BOOLEAN
        ,identity_verified BOOLEAN
    );
    CREATE TABLE IF NOT EXISTS reviews (
        id SERIAL PRIMARY KEY
        ,number_of_reviews INT
        ,first_review DATE
        ,last_review DATE
        ,reviews_per_month NUMERIC(4,2)
        ,rating_score NUMERIC(4,2)
        ,accuracy_score NUMERIC(4,2)
        ,cleanliness_score NUMERIC(4,2)
        ,checkin_score NUMERIC(4,2)
        ,communication_score NUMERIC(4,2)
        ,location_score NUMERIC(4,2)
        ,value_score NUMERIC(4,2)
    );
    CREATE TABLE IF NOT EXISTS listing (
        id SERIAL PRIMARY KEY
        ,listing_url VARCHAR
        ,name VARCHAR
        ,description TEXT
        ,property_type VARCHAR
        ,room_type VARCHAR
        ,accommodates INT
        ,bathrooms_text VARCHAR
        ,bedrooms NUMERIC(3,1)
        ,beds NUMERIC(3,1)
        ,amenities TEXT
        ,price NUMERIC(6,1)
        ,minimum_nights INT
        ,maximum_nights INT
        ,host_id INT
        ,location_id INT
        ,reviews_id INT
    );
    """,
    dag=dag,
)


# ** Using PythonOperator **
insert_data = PythonOperator(
    task_id='load_data',
    python_callable=load_data_to_postgres,
    dag=dag,
)


create_table >> insert_data

# if __name__ == '__main__':
#     load_data_to_postgres()
