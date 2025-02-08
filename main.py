# AUTHOR: NINH GIANG NGUYEN
# PROJECT: Drug's adverse events and Allergic Ingredients Notification System


'''Phase 1: Data Collection (APIs and Web Scraping)'''


import requests
from bs4 import BeautifulSoup


# Fetch drug data using OpenFDA


def fetch_openfda_data(endpoint: str, query: dict):
    base_url = "https://api.fda.gov/drug/"
    url = f"{base_url}{endpoint}.json"
    response = requests.get(url, params = query)
    if response.status_code == 200:
        return response.json()
    else: 
        print(f"Error {response.status_code}: {response.text}")
        return None


# Retrieve drug data using dailyMed


def fetch_dailyMed_data(endpoint: str, drug_name: str):
    base_url = "https://dailymed.nlm.nih.gov/dailymed/services/v2/"
    url = f"{base_url}{endpoint}.json?drug={drug_name}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None


# Retrieve drug data using medlinePlus


def fetch_medlinePlus_data(endpoint: str, query: dict):
    base_url = "https://wsearch.nlm.nih.gov/ws/"
    url = f"{base_url}{endpoint}"
    response = requests.get(url, params=query)
    if response.status_code == 200:
        return response.text  # The response format may vary (XML or plain text)
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None


# Web scrapigng using OpenFDA


def scrape_drug_info(url: str):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    # Extract drug details (modify selectors as needed)
    drug_info = soup.find_all("p")
    return [info.text for info in drug_info]


# COLLECTIONS


open_FDA_endpoints = ["event", "label", "enforcement", "ndc", "drugsfda"]
daily_Med_endpoints = ["drugclasses", "drugnames", "uniis"]
medline_Plus_endpoints = ["query"]

drug_ingredients = fetch_dailyMed_data("uniis", "ibuprofen")
adverse_events = fetch_openfda_data("event", {"limit": 10})

drug_labels = fetch_openfda_data("label", {"limit": 5})

drug_details = scrape_drug_info("https://api.fda.gov/drug/event.json")


'''Phase 2: Data Preprocessing (pandas)'''


import pandas as pd
import re


# Data cleaning by remove_duplicates, handle_missing_values, standardize_text_fields and normalize_numeric_data


def clean_data(data, 
               remove_duplicates = True, 
               handle_missing_values = True, 
               standardize_text_fields = True, 
               normalize_numeric_data = False):
    
    df = pd.DataFrame(data)

    if remove_duplicates: df.drop_duplicates(inplace=True)
    if handle_missing_values: df.fillna("Unknown", inplace=True)

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
            normalized_df[col] = ( df[col] - df[col].min() ) / ( df[col].max() - df[col].min())

            return normalized_df
            
    return df


# Database Schema Desgin


from sqlalchemy import create_engine


# DEFINE THE DATABASE CREDENTIALS


user = 'root'
password = 'password'
host = '127.0.0.1'
port = 3306
database = 'GeeksForGeeks'
 

# Connect Python to the SQL Database


def get_connection():
    return create_engine(
        url="mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
            user, password, host, port, database
        )
    )
try:
    # GET THE CONNECTION OBJECT (ENGINE) FOR THE DATABASE
    engine = get_connection()
    print(
        f"Connection to the {host} for user {user} created successfully.")
except Exception as ex:
    print("Connection could not be made due to the following error: \n", ex)


# Create Tables from Schema in Python


from sqlalchemy import MetaData, Table, Column, Integer, String, Date, Text, ForeignKey


meta = MetaData()

drugs = Table(
    'drugs', meta,
    Column('drug_id', Integer, primary_key=True),
    Column('name', String(255)),
    Column('pharmacologic_class', String(255)),
    Column('unii_list', Text),
    Column('manufacturer', String(255)),
)

recalls = Table(
    'recalls', meta,
    Column('recall_id', Integer, primary_key=True),
    Column('drug_id', Integer, ForeignKey('drugs.drug_id')),
    Column('recall_date', Date),
    Column('recall_reason', Text)
)

adverse_events = Table(
    'adverse_events', meta,
    Column('event_id', Integer, primary_key=True),
    Column('drug_id', Integer, ForeignKey('drugs.drug_id')),
    Column('adverse_event_description', Text)
)

meta.create_all(engine)
print("Tables created successfully!")


# Insert Cleaned Data from Python into SQL Tables




# Insert Data for Recalls, Adverse Events, and drug ingredients

# Query and Verify Data in SQL

# (Optonal) create relationships and advanced querying (Join)

