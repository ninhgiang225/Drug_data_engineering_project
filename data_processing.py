'''AUTHOR: NINH GIANG NGUYEN'''


'''PHASE 2: Data Preprocessing (pandas)'''


import data_collection
import pandas as pd
import re
from sqlalchemy import create_engine, insert, select, func, update
from sqlalchemy import MetaData, Table, Column, Integer, String, Date, Text, ForeignKey, JSON
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, aliased


## DEFINE THE DATABASE CREDENTIALS
user = 'root'
password = 'Giang_020205'
host = 'localhost'
port = 3306
database = 'drugnotificationsystem'


## STEP 1: Data cleaning by remove_duplicates, handle_missing_values, standardize_text_fields and normalize_numeric_data


def clean_data(data, 
               remove_duplicates = False, 
               handle_missing_values = True, 
               standardize_text_fields = True, 
               normalize_numeric_data = False):

    df = pd.DataFrame.from_dict(data)
    
    if remove_duplicates: df.drop_duplicates(inplace=True)
    if handle_missing_values:
        df = df.where(pd.notnull(df), None)

    if standardize_text_fields: 
        for col in df.columns:
            if df[col].dtype == "object":
                df[col] = (
                    df[col].astype(str).str.strip().str.lower()
                    .apply(lambda x: re.sub(r"[^a-z0-9\s]", "", x))
                )

    if normalize_numeric_data:
        normalized_df = df.copy()
        for col in normalized_df.columns:
            if normalized_df[col].dtype == "num":
                normalized_df[col] = ( df[col] - df[col].min() ) / ( df[col].max() - df[col].min())

            return normalized_df
            
    return df


## STEP 2: Database Schema Desgin

 
# Connect Python to the SQL Database


def get_connection():
    return create_engine(
        url="mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
            user, password, host, port, database
        )
    )


# Create Tables from Schema in Python


def create_tables(engine):
    meta = MetaData()

    drugs = Table(
        'drugs', meta,
        Column('drug_id', Integer, primary_key=True),
        Column('type', String(255)),
        Column('name', String(255), nullable=False)
    )

    # Adverse Events table
    adverse_events = Table(
        'adverse_events', meta,
        Column('event_id', Integer, primary_key=True),
        Column('sender', JSON),
        Column('receiver', JSON),
        Column('patient', JSON),
        Column('receivedate', Date),
        Column('reportduplicate', JSON),
        Column('occurcountry', String(255))
    )

    # Recalls table
    recalls = Table(
        'recalls', meta,
        Column('recall_id', Integer, primary_key=True),
        Column('reason_for_recall', Text),
        Column('recall_initiation_date', Date),
        Column('country', String(255))
    )

    meta.create_all(engine)
    print("Tables created successfully!", "\n")

    return meta, drugs, recalls, adverse_events


# Insert Cleaned Data from Python into SQL Tables


def insert_cleaned_data_into_table(table, df, engine):
    with engine.begin() as conn:  # Auto-commit transaction context
        for row in df.to_dict(orient='records'):
            stmt = insert(table).values(**row)
            try:
                conn.execute(stmt)
            except SQLAlchemyError as e:
                print(f"Error inserting data: {e}")


if __name__ == '__main__':

    # Collect data and clean it

    drugs_data = data_collection.fetch_dailyMed_data("drugclasses")
    drugs_data = pd.DataFrame(drugs_data.get('data', []))[["type", "name"]]
    drugs_data = clean_data(drugs_data, remove_duplicates=True)

    adverse_events_data = data_collection.fetch_openfda_data("event", {"limit": 10})
    adverse_events_data = pd.DataFrame(adverse_events_data.get('results', []))[["receivedate","sender", "receiver", "patient", "reportduplicate" , "occurcountry"]]
    adverse_events_data = clean_data(adverse_events_data)
    adverse_events_data['occurcountry'] = adverse_events_data['occurcountry'].replace({"us": "united states"})
    
    recalls_data = data_collection.fetch_openfda_data("enforcement", {"limit": 10})
    recalls_data = pd.DataFrame(recalls_data.get('results', []))[["reason_for_recall", "recall_initiation_date",  "country"]]
    recalls_data = clean_data(recalls_data)

    # Connect Python to the SQL Database

    try:
        engine = get_connection()
        print(
            f"Connection to the {host} for user {user} created successfully!", "\n")
    except Exception as ex:
        print("Connection could not be made due to the following error: \n", ex)
    
    # Create Tables from Schema in Python

    meta, drugs, recalls, adverse_events = create_tables(engine) 
 
    # Insert Cleaned Data from Python into SQL Tables

    print("Inserting drug ingredients...", "\n")
    insert_cleaned_data_into_table(drugs, drugs_data, engine)
  
    
    print("Inserting adverse events...", "\n")
    insert_cleaned_data_into_table(adverse_events, adverse_events_data, engine)

    print("Inserting drug recalls...", "\n")
    insert_cleaned_data_into_table(recalls, recalls_data, engine)

    print("All tables are inserted data successfully! \n")

    # Query and Verify Data in SQL

    print("Example of querying and verifying data in SQL: select the drug recall's reason and date from Mexico \n")
    stmt = select(recalls.c.reason_for_recall, recalls.c.recall_initiation_date).where(recalls.c.country == "mexico").distinct()

    with engine.begin() as conn:
        results = conn.execute(stmt).fetchall()
        for row in results:
            print(row)
    
    # Build Aggregated Queries

    print("\nExample of aggregating queries: return the number of adverse events, and latest recall date of each country \n")
    stmt = (
    select(
        adverse_events.c.occurcountry.label("Country"),
        func.count(adverse_events.c.event_id.distinct()).label("AdverseEventCount"),
        func.max(recalls.c.recall_initiation_date).label("LatestRecallDate"),
        )
    .select_from(adverse_events.join(recalls, adverse_events.c.occurcountry == recalls.c.country))
    .group_by(adverse_events.c.occurcountry)
    )

    with engine.connect() as conn:
        results = conn.execute(stmt).fetchall()
        for row in results:
            print(row)

    chosen_layer_df = pd.read_sql(stmt, engine)
    print("\n", chosen_layer_df)



    






