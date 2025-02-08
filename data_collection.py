'''AUTHOR: NINH GIANG NGUYEN'''


'''PHASE 1: Data Collection (APIs and Web Scraping)'''


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


def fetch_dailyMed_data(endpoint: str):
    base_url = "https://dailymed.nlm.nih.gov/dailymed/services/v2/"
    url = f"{base_url}{endpoint}.json"
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


# Endpoints


open_FDA_endpoints = ["event", "label", "enforcement", "ndc", "drugsfda"]
daily_Med_endpoints = ["drugclasses", "drugnames", "uniis"]
medline_Plus_endpoints = ["query"]


if __name__ == '__main__':

    # Extracted data from API and web scraping

    drug_ingredients = fetch_dailyMed_data("drugclasses")
    adverse_events = fetch_openfda_data("event", {"limit": 10})

    drug_labels = fetch_openfda_data("label", {"limit": 5})

    drug_details = scrape_drug_info("https://api.fda.gov/drug/event.json")

    print(adverse_events)