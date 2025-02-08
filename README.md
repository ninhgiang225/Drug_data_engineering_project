# Drug Data Engineering Project

**Author:** Ninh Giang Nguyen

## Overview
This project is a comprehensive system designed to collect, process, and visualize drug information. It has potential applications for pharmacists, healthcare providers, and consumers seeking to manage medications safely. The project bridges the gap between data engineering and health data science.

## Key Features

### **Data Collection**
- Fetches drug data from APIs like OpenFDA, DailyMed, and MedlinePlus.
- Includes web scraping to extract additional drug information.

### **Data Preprocessing**
- Cleans and normalizes data to handle missing values, standardizes text fields, and removes duplicates.
- Stores structured data in a MySQL relational database with three tables:  
  - **Drug Details**
  - **Recall Tracking**
  - **Adverse Event Notifications**

### **Data Visualization**
- Observes the distribution of data using visualizations like word clouds, pie charts, and more.
- Displays outputs from data processing for analysis.

## Technologies Used
- **Programming Languages:** Python
- **APIs:** OpenFDA, DailyMed, MedlinePlus
- **Data Processing:** Pandas
- **Database:** MySQL
- **Web Scraping:** BeautifulSoup
- **ORM:** SQLAlchemy
- **Visualization:** Seaborn, Wordcloud, Plotly

---

## Setup and Installation

### **Prerequisites**
- Python 3.x
- MySQL
- Pipenv or virtual environment
- API access credentials (if required for OpenFDA/DailyMed)

### **Installation**
1. Clone the repository:
   ```bash
   git clone https://github.com/ninhgiangnguyen/Drug_data_engineering_project.git
   cd Drug_data_engineering_project
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv env
   source env/bin/activate  # For Linux/MacOS
   env\Scripts\activate     # For Windows
3. Install the required packages:
   ```bash
   pip install -r requirements.txt
4. Run the data collection script to fetch drug information, then clean the data and store it in the SQL database:
   ```bash
   python data_collection.py
   python data_preprocessing.py

## Challenges and Future Improvements
- Limited Data Access: Due to the sensitive nature of drug data, access was restricted, making it difficult to train models or make predictions.
- Focus on Data Engineering: The project focused on data extraction, storage in SQL, and cleaning instead of analytics or modeling.
- Data Access: Secure licensed datasets for better insights and model training.
- Advanced Analytics: Develop predictive models once data constraints are resolved.
- Data Enrichment: Explore additional data sources and optimize collection methods.
   
